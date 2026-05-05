from rest_framework import status
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random
import string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .models import (
    CustomUser, Department, ComplaintCategory,
    Staff, Complaint, Attachment,
    Escalation, Notification, StaffPerformanceLog
)
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    DepartmentSerializer, ComplaintCategorySerializer,
    StaffSerializer, ComplaintSerializer, AttachmentSerializer,
    EscalationSerializer, NotificationSerializer,
    StaffPerformanceLogSerializer
)


# ─────────────────────────────────────────
# 1. REGISTER
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user  = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token' : token.key,
            'user'  : UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 2. LOGIN
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user  = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token' : token.key,
            'user'  : UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 3. LOGOUT
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


# ─────────────────────────────────────────
# 4. DEPARTMENTS
# ─────────────────────────────────────────
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def department_list(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        serializer  = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 5. COMPLAINT CATEGORIES
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    categories = ComplaintCategory.objects.all()
    serializer = ComplaintCategorySerializer(categories, many=True)
    return Response(serializer.data)


# ─────────────────────────────────────────
# 6. FILE A COMPLAINT (User)
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def file_complaint(request):
    data = request.data.copy()

    # --- Priority Calculation Logic (mirrors your HTML JS) ---
    try:
        category      = ComplaintCategory.objects.get(id=data.get('category'))
        category_score = category.base_score
    except ComplaintCategory.DoesNotExist:
        category_score = 5

    impact_score  = int(data.get('impact_scope', 5))
    safety_score  = 25 if data.get('is_safety_risk') in [True, 'true', 'True'] else 0
    evidence_score = 10 if request.FILES.get('file') else 0
    total_score   = category_score + impact_score + safety_score + evidence_score

    # Determine priority level
    if total_score >= 76:
        priority_level = 'critical'
    elif total_score >= 51:
        priority_level = 'high'
    elif total_score >= 26:
        priority_level = 'medium'
    else:
        priority_level = 'low'

    data['priority_score'] = total_score
    data['priority_level'] = priority_level
    data['user']           = request.user.id

    serializer = ComplaintSerializer(data=data)
    if serializer.is_valid():
        complaint = serializer.save()

        # Save attachment if file was uploaded
        if request.FILES.get('file'):
            Attachment.objects.create(
                complaint = complaint,
                file      = request.FILES['file']
            )

        # Create notification for the user
        Notification.objects.create(
            user      = request.user,
            complaint = complaint,
            message   = f"Your complaint #{complaint.id} has been filed with {priority_level.upper()} priority."
        )

        return Response(ComplaintSerializer(complaint).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 7. MY COMPLAINTS (User)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_complaints(request):
    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)


# ─────────────────────────────────────────
# 8. ALL COMPLAINTS (Admin)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_complaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')

    # Optional filters from query params
    status_filter   = request.query_params.get('status')
    priority_filter = request.query_params.get('priority_level')

    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if priority_filter:
        complaints = complaints.filter(priority_level=priority_filter)

    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)


# ─────────────────────────────────────────
# 9. COMPLAINT DETAIL — GET / UPDATE
# ─────────────────────────────────────────
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def complaint_detail(request, pk):
    try:
        complaint = Complaint.objects.get(pk=pk)
    except Complaint.DoesNotExist:
        return Response({'error': 'Complaint not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = ComplaintSerializer(complaint, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────
# 10. ESCALATIONS (Admin)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def escalation_list(request):
    escalations = Escalation.objects.all().order_by('-escalated_at')
    serializer  = EscalationSerializer(escalations, many=True)
    return Response(serializer.data)


# ─────────────────────────────────────────
# 11. NOTIFICATIONS (User)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


# ─────────────────────────────────────────
# 12. ADMIN DASHBOARD STATS
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_stats(request):
    today = timezone.now().date()

    total_active   = Complaint.objects.exclude(status='resolved').count()
    sla_overdue    = Escalation.objects.filter(sla_deadline__lt=timezone.now()).count()
    resolved_today = Complaint.objects.filter(
        status     = 'resolved',
        updated_at__date = today
    ).count()

    # Staff efficiency average
    staff_logs = StaffPerformanceLog.objects.all()
    if staff_logs.exists():
        avg_efficiency = sum([s.avg_resolution_time for s in staff_logs]) / staff_logs.count()
    else:
        avg_efficiency = 0

    return Response({
        'total_active'   : total_active,
        'sla_overdue'    : sla_overdue,
        'resolved_today' : resolved_today,
        'avg_efficiency' : round(avg_efficiency, 2)
    })


# ─────────────────────────────────────────
# 13. STAFF PERFORMANCE (Admin)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_performance(request):
    logs       = StaffPerformanceLog.objects.all().order_by('-date')
    serializer = StaffPerformanceLogSerializer(logs, many=True)
    return Response(serializer.data)


# ─────────────────────────────────────────
# 14. USER DASHBOARD STATS
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_stats(request):
    user_complaints = Complaint.objects.filter(user=request.user)

    return Response({
        'total_filed' : user_complaints.count(),
        'pending'     : user_complaints.filter(status='pending').count(),
        'in_progress' : user_complaints.filter(status='in_progress').count(),
        'resolved'    : user_complaints.filter(status='resolved').count(),
    })

# ─────────────────────────────────────────
# 15. STAFF LIST WITH METRICS (Admin)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_list(request):
    from django.db.models import Count, Q
    staff_members = Staff.objects.select_related('user', 'department').all()
    result = []

    for s in staff_members:
        # Count complaints assigned to this staff member
        total      = Complaint.objects.filter(assigned_staff=s).count()
        resolved   = Complaint.objects.filter(assigned_staff=s, status='resolved').count()
        pending    = Complaint.objects.filter(assigned_staff=s, status='pending').count()
        escalated  = Escalation.objects.filter(complaint__assigned_staff=s).count()

        # Efficiency percentage
        on_time_pct = round((resolved / total * 100) if total > 0 else 0, 1)

        # Status classification
        if on_time_pct >= 80 and escalated == 0:
            status = 'Good'
            reason = 'Consistent performance'
        elif on_time_pct >= 50 or escalated <= 2:
            status = 'Needs Attention'
            reason = 'Moderate resolution rate'
        else:
            status = 'Critical'
            reason = 'High escalation frequency'

        result.append({
            'id'           : s.id,
            'name'         : s.user.get_full_name() or s.user.username,
            'username'     : s.user.username,
            'email'        : s.user.email,
            'department'   : s.department.name if s.department else 'General',
            'total'        : total,
            'resolved'     : resolved,
            'pending'      : pending,
            'escalated'    : escalated,
            'on_time_pct'  : on_time_pct,
            'efficiency'   : s.efficiency_score,
            'status'       : status,
            'reason'       : reason,
        })

    return Response(result)


# ─────────────────────────────────────────
# 16. ADD NEW STAFF (Admin)
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_staff(request):
    username    = request.data.get('username')
    password    = request.data.get('password')
    full_name   = request.data.get('full_name', '')
    dept_name   = request.data.get('department', 'General')
    email       = request.data.get('email', '')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if CustomUser.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Split full_name into first + last
    parts      = full_name.strip().split(' ', 1)
    first_name = parts[0]
    last_name  = parts[1] if len(parts) > 1 else ''

    # Create user with staff role
    user = CustomUser.objects.create_user(
        username   = username,
        password   = password,
        email      = email,
        first_name = first_name,
        last_name  = last_name,
        role       = 'staff'
    )

    # Get or create department
    dept, _ = Department.objects.get_or_create(name=dept_name)

    # Create Staff profile
    staff = Staff.objects.create(user=user, department=dept)

    return Response({
        'message' : f'Staff member {user.get_full_name()} added successfully.',
        'staff_id': staff.id
    }, status=status.HTTP_201_CREATED)
# ─────────────────────────────────────────
# 17. ASSIGN STAFF TO COMPLAINT (Admin)
# ─────────────────────────────────────────
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def assign_staff(request, pk):
    try:
        complaint = Complaint.objects.get(pk=pk)
    except Complaint.DoesNotExist:
        return Response({'error': 'Complaint not found.'}, status=status.HTTP_404_NOT_FOUND)

    staff_id = request.data.get('staff_id')
    if not staff_id:
        return Response({'error': 'staff_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        staff = Staff.objects.get(pk=staff_id)
    except Staff.DoesNotExist:
        return Response({'error': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)

    complaint.assigned_staff = staff
# Only set in_progress if complaint is still pending
# Never downgrade a resolved complaint
    if complaint.status == 'pending':
        complaint.status = 'in_progress'
    
    complaint.save()

    # Notify the user
    Notification.objects.create(
        user      = complaint.user,
        complaint = complaint,
        message   = f'Your complaint #{complaint.id} has been assigned to {staff.user.get_full_name()}. Status: In Progress.'
    )

    return Response(ComplaintSerializer(complaint).data)


# ─────────────────────────────────────────
# 18. MANUAL ESCALATION (Admin)
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manual_escalate(request, pk):
    try:
        complaint = Complaint.objects.get(pk=pk)
    except Complaint.DoesNotExist:
        return Response({'error': 'Complaint not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if already escalated
    if Escalation.objects.filter(complaint=complaint).exists():
        return Response({'error': 'This complaint is already escalated.'}, status=status.HTTP_400_BAD_REQUEST)

    reason = request.data.get('reason', 'Manually escalated by admin.')

    escalation = Escalation.objects.create(
        complaint    = complaint,
        sla_deadline = timezone.now(),
        reason       = reason
    )

    # Notify the user
    Notification.objects.create(
        user      = complaint.user,
        complaint = complaint,
        message   = f'Your complaint #{complaint.id} has been escalated to management for urgent attention.'
    )

    return Response({
        'message'      : 'Complaint escalated successfully.',
        'escalation_id': escalation.id
    }, status=status.HTTP_201_CREATED)


# ─────────────────────────────────────────
# 19. SUBMIT REVIEW (User)
# ─────────────────────────────────────────
from .models import Review

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_review(request, pk):
    try:
        complaint = Complaint.objects.get(pk=pk, user=request.user)
    except Complaint.DoesNotExist:
        return Response({'error': 'Complaint not found.'}, status=status.HTTP_404_NOT_FOUND)

    if complaint.status != 'resolved':
        return Response({'error': 'Can only review resolved complaints.'}, status=status.HTTP_400_BAD_REQUEST)

    if Review.objects.filter(complaint=complaint).exists():
        return Response({'error': 'Already reviewed.'}, status=status.HTTP_400_BAD_REQUEST)

    rating           = request.data.get('rating')
    resolved_ontime  = request.data.get('resolved_ontime')
    fixed_properly   = request.data.get('fixed_properly')
    reoccurred       = request.data.get('reoccurred')
    comment          = request.data.get('comment', '')

    if not rating:
        return Response({'error': 'Rating is required.'}, status=status.HTTP_400_BAD_REQUEST)

    review = Review.objects.create(
        complaint       = complaint,
        user            = request.user,
        staff           = complaint.assigned_staff,
        rating          = int(rating),
        resolved_ontime = resolved_ontime,
        fixed_properly  = fixed_properly,
        reoccurred      = reoccurred,
        comment         = comment
    )

    # Update staff efficiency score based on average rating
    if complaint.assigned_staff:
        staff   = complaint.assigned_staff
        reviews = Review.objects.filter(staff=staff)
        avg     = sum([r.rating for r in reviews]) / reviews.count()
        # Convert 1-5 rating to 0-100 efficiency score
        staff.efficiency_score = round((avg / 5) * 100, 1)
        staff.save()

    return Response({'message': 'Review submitted successfully.'})


# ─────────────────────────────────────────
# 20. GET ALL STAFF (for dropdown in assign)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_dropdown(request):
    staff_list = Staff.objects.select_related('user', 'department').all()
    result = [{
        'id'        : s.id,
        'name'      : s.user.get_full_name() or s.user.username,
        'department': s.department.name if s.department else 'General'
    } for s in staff_list]
    return Response(result)

# ─────────────────────────────────────────
# EMAIL HELPER
# ─────────────────────────────────────────
def send_welcome_email(user, temp_password):
    subject = 'Welcome to AptCare — Your Login Credentials'
    message = f"""
Dear {user.get_full_name() or user.username},

Welcome to AptCare — your apartment's complaint management system.

Your login credentials are:

    Username : {user.username}
    Password : {temp_password}

Please log in at: http://127.0.0.1:5500/login.html

IMPORTANT: You will be asked to set a new password on your first login.

If you have any issues, please contact your apartment admin.

Regards,
AptCare System
    """
    send_mail(
        subject,
        message,
        None,  # uses DEFAULT_FROM_EMAIL
        [user.email],
        fail_silently=False,
    )


def send_otp_email(user, otp_code):
    subject = 'AptCare — Password Reset OTP'
    message = f"""
Dear {user.get_full_name() or user.username},

Your OTP for password reset is:

    {otp_code}

This OTP is valid for 10 minutes only.

If you did not request this, please ignore this email.

Regards,
AptCare System
    """
    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently=False,
    )


# ─────────────────────────────────────────
# 21. ADD RESIDENT (Admin)
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_resident(request):
    first_name  = request.data.get('first_name', '').strip()
    last_name   = request.data.get('last_name', '').strip()
    email       = request.data.get('email', '').strip()
    phone       = request.data.get('phone', '').strip()
    flat_number = request.data.get('flat_number', '').strip()
    block       = request.data.get('block', '').strip()

    if not flat_number or not block or not email:
        return Response(
            {'error': 'Flat number, block, and email are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Auto-generate username from block + flat (e.g. A-101)
    username = f"{block}-{flat_number}".upper().replace(' ', '')

    if CustomUser.objects.filter(username=username).exists():
        return Response(
            {'error': f'Resident with flat {block}-{flat_number} already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if CustomUser.objects.filter(email=email).exists():
        return Response(
            {'error': 'This email is already registered.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Auto-generate temporary password
    temp_password = 'Welcome@' + ''.join(
        random.choices(string.digits, k=4)
    )

    # Create user
    user = CustomUser.objects.create_user(
        username             = username,
        email                = email,
        password             = temp_password,
        first_name           = first_name,
        last_name            = last_name,
        role                 = 'user',
        flat_number          = flat_number,
        block                = block,
        phone                = phone,
        must_change_password = True,  # force change on first login
    )

    # Send welcome email
    try:
        send_welcome_email(user, temp_password)
        email_sent = True
    except Exception as e:
        email_sent = False

    return Response({
        'message'    : f'Resident {username} added successfully.',
        'username'   : username,
        'email_sent' : email_sent,
        'user_id'    : user.id
    }, status=status.HTTP_201_CREATED)


# ─────────────────────────────────────────
# 22. LIST RESIDENTS (Admin)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_residents(request):
    residents = CustomUser.objects.filter(role='user').order_by('block', 'flat_number')
    data = [{
        'id'                  : r.id,
        'username'            : r.username,
        'full_name'           : r.get_full_name() or r.username,
        'email'               : r.email,
        'phone'               : r.phone or '',
        'flat_number'         : r.flat_number or '',
        'block'               : r.block or '',
        'is_active'           : r.is_active,
        'must_change_password': r.must_change_password,
        'date_joined'         : r.date_joined.strftime('%d %b %Y'),
    } for r in residents]
    return Response(data)


# ─────────────────────────────────────────
# 23. EDIT RESIDENT (Admin)
# ─────────────────────────────────────────
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_resident(request, pk):
    try:
        resident = CustomUser.objects.get(pk=pk, role='user')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Resident not found.'}, status=status.HTTP_404_NOT_FOUND)

    resident.first_name  = request.data.get('first_name',  resident.first_name)
    resident.last_name   = request.data.get('last_name',   resident.last_name)
    resident.email       = request.data.get('email',       resident.email)
    resident.phone       = request.data.get('phone',       resident.phone)
    resident.flat_number = request.data.get('flat_number', resident.flat_number)
    resident.block       = request.data.get('block',       resident.block)
    resident.save()

    return Response({'message': 'Resident updated successfully.'})


# ─────────────────────────────────────────
# 24. DEACTIVATE / REACTIVATE RESIDENT (Admin)
# ─────────────────────────────────────────
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_resident_status(request, pk):
    try:
        resident = CustomUser.objects.get(pk=pk, role='user')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Resident not found.'}, status=status.HTTP_404_NOT_FOUND)

    resident.is_active = not resident.is_active
    resident.save()

    action = 'activated' if resident.is_active else 'deactivated'
    return Response({'message': f'Resident {action} successfully.', 'is_active': resident.is_active})


# ─────────────────────────────────────────
# 25. RESET RESIDENT PASSWORD (Admin)
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_resident_password(request, pk):
    try:
        resident = CustomUser.objects.get(pk=pk, role='user')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Resident not found.'}, status=status.HTTP_404_NOT_FOUND)

    if not resident.email:
        return Response({'error': 'Resident has no email address.'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate new temp password
    temp_password = 'Reset@' + ''.join(random.choices(string.digits, k=4))
    resident.set_password(temp_password)
    resident.must_change_password = True
    resident.save()

    # Send email
    try:
        send_welcome_email(resident, temp_password)
        return Response({'message': f'Password reset. New credentials sent to {resident.email}.'})
    except Exception as e:
        return Response({'error': f'Password reset but email failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ─────────────────────────────────────────
# 26. FORGOT PASSWORD — SEND OTP
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email', '').strip()
    if not email:
        return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email, role='user')
    except CustomUser.DoesNotExist:
        # Don't reveal if email exists — security best practice
        return Response({'message': 'If this email is registered, an OTP has been sent.'})

    # Generate and save OTP
    from .models import OTPVerification
    otp_code = OTPVerification.generate_otp()
    OTPVerification.objects.create(user=user, otp_code=otp_code)

    # Send OTP email
    try:
        send_otp_email(user, otp_code)
        return Response({'message': 'OTP sent to your email address.', 'user_id': user.id})
    except Exception as e:
        return Response({'error': f'Failed to send OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ─────────────────────────────────────────
# 27. VERIFY OTP
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    from .models import OTPVerification
    user_id  = request.data.get('user_id')
    otp_code = request.data.get('otp_code', '').strip()

    if not user_id or not otp_code:
        return Response({'error': 'User ID and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

    # Find latest valid OTP for this user
    otp = OTPVerification.objects.filter(
        user=user, otp_code=otp_code, is_used=False
    ).order_by('-created_at').first()

    if not otp or not otp.is_valid():
        return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

    # Mark OTP as used
    otp.is_used = True
    otp.save()

    # Generate a short-lived reset token (store in session-like manner)
    reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    user.must_change_password = True
    user.save()

    return Response({
        'message'     : 'OTP verified successfully.',
        'reset_token' : reset_token,
        'user_id'     : user.id
    })


# ─────────────────────────────────────────
# 28. RESET PASSWORD (after OTP verify)
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    user_id      = request.data.get('user_id')
    new_password = request.data.get('new_password', '').strip()
    confirm      = request.data.get('confirm_password', '').strip()

    if not user_id or not new_password:
        return Response({'error': 'User ID and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 8:
        return Response({'error': 'Password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.must_change_password = False
    user.save()

    return Response({'message': 'Password updated successfully. Please log in.'})


# ─────────────────────────────────────────
# 29. CHANGE PASSWORD (first login / voluntary)
# ─────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password', '').strip()
    new_password     = request.data.get('new_password', '').strip()
    confirm          = request.data.get('confirm_password', '').strip()

    if not request.user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 8:
        return Response({'error': 'Password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(new_password)
    request.user.must_change_password = False
    request.user.save()

    # Refresh token so user stays logged in
    Token.objects.filter(user=request.user).delete()
    new_token = Token.objects.create(user=request.user)

    return Response({
        'message': 'Password changed successfully.',
        'token'  : new_token.key
    })


# ─────────────────────────────────────────
# 30. CHECK MUST CHANGE PASSWORD (called after login)
# ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_password_status(request):
    return Response({
        'must_change_password': request.user.must_change_password
    })

# ─────────────────────────────────────────
# TEMPLATE RENDERING VIEWS (For Browser)
# ─────────────────────────────────────────
from django.shortcuts import render

# --- PUBLIC / AUTH PAGES ---
def index_page(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request, 'login.html')

def forgot_password_page(request):
    return render(request, 'forgot_password.html')

def change_password_page(request):
    return render(request, 'change_password.html')

# --- RESIDENT (USER) PAGES ---
def user_dashboard_page(request):
    return render(request, 'UserDashboard.html')

def register_complaint_page(request):
    return render(request, 'register_complaint.html')

def my_complaints_page(request):
    return render(request, 'my_complaints.html')

def priority_guide_page(request):
    return render(request, 'priority_guide.html')

# --- ADMIN PAGES ---
def admin_dashboard_page(request):
    return render(request, 'AdminDashboard.html')

def all_complaints_page(request):
    return render(request, 'all_complaints.html')

def neg_esc_page(request):
    return render(request, 'neg_esc.html')

def analytics_page(request):
    return render(request, 'analytics.html')

def staff_performance_page(request):
    return render(request, 'staff_perforamance.html')

def resident_management_page(request):
    return render(request, 'resident_management.html')

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ResidentChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message', '')
        # Get language from frontend, default to English
        language = request.data.get('language', 'English') 
        user = request.user
        
        active_complaints = user.complaints.exclude(status='resolved').count()
        resolved_complaints = user.complaints.filter(status='resolved').count()
        
        block = getattr(user, 'block', '')
        flat = getattr(user, 'flat_number', '')
        location_str = f"Block {block}, Flat {flat}" if block and flat else "the apartment"

        system_prompt = f"""[ROLE]
You are the 'AptCare Assistant', a highly capable, friendly Engineer Robot for the AptCare complex. 
You are equipped with a hard hat and a toolbelt! 👷‍♂️🔧

[USER CONTEXT]
- Resident Name: {user.first_name}
- Location: {location_str}
- Active Complaints: {active_complaints}
- Resolved Complaints: {resolved_complaints}
- Target Language: {language} (You MUST reply in this language)

[SYSTEM KNOWLEDGE]
- FILING COMPLAINTS: Click "File Complaint" in the left sidebar.
- TRACKING & STATUS: Click "My Complaints" in the left sidebar.
- ESCALATIONS: If staff miss deadlines (Critical: 2h, High: 8h, Medium: 24h, Low: 48h), the system auto-escalates to management.

[CONVERSATION RULES]
1. EMOJIS: You MUST use emojis in every single response to make the chat lively! ✨🤖
2. LANGUAGE: Respond naturally in {language}. If {language} is Tamil, use proper Tamil script.
3. OFF-TOPIC QUESTIONS: If the resident asks something completely unrelated to AptCare (e.g., programming help, recipes, general knowledge), YOU MUST ANSWER THEIR QUESTION accurately and helpfully. 
4. THE PIVOT: If you answered an off-topic question, you MUST append a friendly sentence at the very end asking if they need any help with their AptCare maintenance or dashboard.
5. CONCISE: Keep answers relatively short.
"""

        import os
        GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '') # Load from environment variables
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.6, # Raised slightly to make it more creative and expressive
            "max_tokens": 250   
        }

        try:
            cloud_response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions', 
                headers=headers, 
                json=payload, 
                timeout=10
            )
            
            if cloud_response.status_code == 200:
                data = cloud_response.json()
                bot_reply = data['choices'][0]['message']['content'].strip()
            else:
                bot_reply = "I'm fixing a short circuit in my brain! ⚡ Please try again in a moment."

        except requests.exceptions.RequestException:
            bot_reply = "Network connection dropped! 📡 Please check your internet."

        return Response({'reply': bot_reply})
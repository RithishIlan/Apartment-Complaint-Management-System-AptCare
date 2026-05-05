from django.db import models
from django.contrib.auth.models import AbstractUser


# ─────────────────────────────────────────
# 1. CUSTOM USER
# ─────────────────────────────────────────
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('staff', 'Staff'),
    ]
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    flat_number = models.CharField(max_length=20, blank=True, null=True)
    block       = models.CharField(max_length=20, blank=True, null=True)
    phone       = models.CharField(max_length=15, blank=True, null=True)
    must_change_password = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"


# ─────────────────────────────────────────
# 2. DEPARTMENT
# ─────────────────────────────────────────
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────
# 3. COMPLAINT CATEGORY
# ─────────────────────────────────────────
class ComplaintCategory(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    base_score  = models.IntegerField(default=5)  # from HTML option values
    department  = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────
# 4. STAFF
# ─────────────────────────────────────────
class Staff(models.Model):
    user            = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department      = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    efficiency_score = models.FloatField(default=100.0)

    def __str__(self):
        return self.user.get_full_name()


# ─────────────────────────────────────────
# 5. COMPLAINT
# ─────────────────────────────────────────
class Complaint(models.Model):

    IMPACT_CHOICES = [
        (5,  'My Flat Only'),
        (10, 'One Floor / Corridor'),
        (15, 'Multiple Floors'),
        (20, 'Entire Block / Building'),
        (18, 'Common Area'),
    ]

    PRIORITY_CHOICES = [
        ('low',      'Low'),
        ('medium',   'Medium'),
        ('high',     'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved',    'Resolved'),
    ]

    user            = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints')
    category        = models.ForeignKey(ComplaintCategory, on_delete=models.SET_NULL, null=True)
    location        = models.CharField(max_length=255)
    impact_scope    = models.IntegerField(choices=IMPACT_CHOICES, default=5)
    is_safety_risk  = models.BooleanField(default=False)
    description     = models.TextField()
    priority_score  = models.IntegerField(default=0)
    priority_level  = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    status          = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    assigned_staff  = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.category} ({self.priority_level})"


# ─────────────────────────────────────────
# 6. ATTACHMENT
# ─────────────────────────────────────────
class Attachment(models.Model):
    complaint   = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    file        = models.FileField(upload_to='complaint_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Complaint #{self.complaint.id}"


# ─────────────────────────────────────────
# 7. ESCALATION
# ─────────────────────────────────────────
class Escalation(models.Model):
    complaint    = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='escalation')
    sla_deadline = models.DateTimeField()
    escalated_at = models.DateTimeField(auto_now_add=True)
    reason       = models.TextField(blank=True)

    def __str__(self):
        return f"Escalation for Complaint #{self.complaint.id}"


# ─────────────────────────────────────────
# 8. NOTIFICATION
# ─────────────────────────────────────────
class Notification(models.Model):
    user        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    complaint   = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True, blank=True)
    message     = models.TextField()
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


# ─────────────────────────────────────────
# 9. STAFF PERFORMANCE LOG
# ─────────────────────────────────────────
class StaffPerformanceLog(models.Model):
    staff                = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='performance_logs')
    complaints_resolved  = models.IntegerField(default=0)
    avg_resolution_time  = models.FloatField(default=0.0)  # in hours
    date                 = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.date}"

# ─────────────────────────────────────────
# 10. REVIEW (User rates resolved complaint)
# ─────────────────────────────────────────
class Review(models.Model):
    complaint     = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='review')
    user          = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    staff         = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    rating        = models.IntegerField()  # 1 to 5
    resolved_ontime = models.BooleanField(null=True, blank=True)
    fixed_properly  = models.BooleanField(null=True, blank=True)
    reoccurred      = models.BooleanField(null=True, blank=True)
    comment       = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Complaint #{self.complaint.id} — {self.rating}★"

# ─────────────────────────────────────────
# 11. OTP (for Forgot Password)
# ─────────────────────────────────────────
import random
import string
from django.utils import timezone

class OTPVerification(models.Model):
    user       = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    otp_code   = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def is_valid(self):
        # OTP expires after 10 minutes
        expiry = self.created_at + timezone.timedelta(minutes=10)
        return not self.is_used and timezone.now() < expiry

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))

    def __str__(self):
        return f"OTP for {self.user.username} — {self.otp_code}"
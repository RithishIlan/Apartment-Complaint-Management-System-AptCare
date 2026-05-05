from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    CustomUser, Department, ComplaintCategory,
    Staff, Complaint, Attachment,
    Escalation, Notification, StaffPerformanceLog
)


# ─────────────────────────────────────────
# 1. USER SERIALIZERS
# ─────────────────────────────────────────
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model  = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'flat_number', 'block', 'phone']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username    = validated_data['username'],
            email       = validated_data.get('email', ''),
            password    = validated_data['password'],
            role        = validated_data.get('role', 'user'),
            flat_number = validated_data.get('flat_number', ''),
            block       = validated_data.get('block', ''),
            phone       = validated_data.get('phone', ''),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username = data['username'],
            password = data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CustomUser
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'must_change_password']

# ─────────────────────────────────────────
# 2. DEPARTMENT SERIALIZER
# ─────────────────────────────────────────
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Department
        fields = '__all__'


# ─────────────────────────────────────────
# 3. COMPLAINT CATEGORY SERIALIZER
# ─────────────────────────────────────────
class ComplaintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ComplaintCategory
        fields = '__all__'


# ─────────────────────────────────────────
# 4. STAFF SERIALIZER
# ─────────────────────────────────────────
class StaffSerializer(serializers.ModelSerializer):
    user       = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model  = Staff
        fields = '__all__'


# ─────────────────────────────────────────
# 5. ATTACHMENT SERIALIZER
# ─────────────────────────────────────────
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Attachment
        fields = '__all__'


# ─────────────────────────────────────────
# 6. COMPLAINT SERIALIZER
# ─────────────────────────────────────────
class ComplaintSerializer(serializers.ModelSerializer):
    # Your existing fields
    attachments   = AttachmentSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    user_name     = serializers.CharField(source='user.username', read_only=True)
    staff_name    = serializers.CharField(source='assigned_staff.user.get_full_name', read_only=True)
    
    # NEW: A dedicated field that just sends the direct image URL
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model  = Complaint
        fields = '__all__'
        read_only_fields = ['priority_score', 'priority_level', 'created_at', 'updated_at']

    # NEW: The function that grabs the exact photo link
    def get_attachment_url(self, obj):
        # We look inside the attachments related to this specific complaint
        attachment = obj.attachments.first() 
        if attachment and attachment.file:
            return attachment.file.url
        return None


# ─────────────────────────────────────────
# 7. ESCALATION SERIALIZER
# ─────────────────────────────────────────
class EscalationSerializer(serializers.ModelSerializer):
    complaint = ComplaintSerializer(read_only=True)

    class Meta:
        model  = Escalation
        fields = '__all__'


# ─────────────────────────────────────────
# 8. NOTIFICATION SERIALIZER
# ─────────────────────────────────────────
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Notification
        fields = '__all__'


# ─────────────────────────────────────────
# 9. STAFF PERFORMANCE LOG SERIALIZER
# ─────────────────────────────────────────
class StaffPerformanceLogSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.user.get_full_name', read_only=True)

    class Meta:
        model  = StaffPerformanceLog
        fields = '__all__'
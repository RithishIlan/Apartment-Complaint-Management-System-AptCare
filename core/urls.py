from django.urls import path
from . import views
from .views import ResidentChatbotView

urlpatterns = [

    # ─────────────────────────────────────────
    # AUTH
    # ─────────────────────────────────────────
    path('auth/register/',  views.register_view,  name='register'),
    path('auth/login/',     views.login_view,      name='login'),
    path('auth/logout/',    views.logout_view,     name='logout'),

    # ─────────────────────────────────────────
    # DEPARTMENTS & CATEGORIES
    # ─────────────────────────────────────────
    path('departments/',    views.department_list, name='department-list'),
    path('categories/',     views.category_list,   name='category-list'),

    # ─────────────────────────────────────────
    # COMPLAINTS
    # ─────────────────────────────────────────
    path('complaints/file/',         views.file_complaint,   name='file-complaint'),
    path('complaints/mine/',         views.my_complaints,    name='my-complaints'),
    path('complaints/all/',          views.all_complaints,   name='all-complaints'),
    path('complaints/<int:pk>/',     views.complaint_detail, name='complaint-detail'),

    # ─────────────────────────────────────────
    # ESCALATIONS
    # ─────────────────────────────────────────
    path('escalations/',    views.escalation_list,  name='escalation-list'),

    # ─────────────────────────────────────────
    # NOTIFICATIONS
    # ─────────────────────────────────────────
    path('notifications/',  views.my_notifications, name='my-notifications'),

    # ─────────────────────────────────────────
    # DASHBOARD STATS
    # ─────────────────────────────────────────
    path('dashboard/admin/', views.admin_dashboard_stats, name='admin-dashboard'),
    path('dashboard/user/',  views.user_dashboard_stats,  name='user-dashboard'),

    # ─────────────────────────────────────────
    # STAFF
    # ─────────────────────────────────────────
    path('staff/performance/', views.staff_performance, name='staff-performance'),
    # Staff
path('staff/',          views.staff_list, name='staff-list'),
path('staff/add/',      views.add_staff,  name='add-staff'),
# Assign staff + escalation
path('complaints/<int:pk>/assign/',   views.assign_staff,   name='assign-staff'),
path('complaints/<int:pk>/escalate/', views.manual_escalate, name='manual-escalate'),

# Review
path('complaints/<int:pk>/review/',   views.submit_review,  name='submit-review'),

# Staff dropdown
path('staff/dropdown/',               views.staff_dropdown,  name='staff-dropdown'),
# Resident Management
path('residents/',                    views.list_residents,          name='list-residents'),
path('residents/add/',                views.add_resident,            name='add-resident'),
path('residents/<int:pk>/edit/',      views.edit_resident,           name='edit-resident'),
path('residents/<int:pk>/toggle/',    views.toggle_resident_status,  name='toggle-resident'),
path('residents/<int:pk>/reset-password/', views.reset_resident_password, name='reset-resident-password'),

# Password Management
path('auth/forgot-password/',   views.forgot_password,        name='forgot-password'),
path('auth/verify-otp/',        views.verify_otp,             name='verify-otp'),
path('auth/reset-password/',    views.reset_password,         name='reset-password'),
path('auth/change-password/',   views.change_password,        name='change-password'),
path('auth/password-status/',   views.check_password_status,  name='password-status'),
# Add this import at the top


# Add this to your urlpatterns list:
path('chatbot/', ResidentChatbotView.as_view(), name='resident-chatbot'),
]
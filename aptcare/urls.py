from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import all 14 template views
from core.views import (
    index_page, login_page, forgot_password_page, change_password_page,
    user_dashboard_page, register_complaint_page, my_complaints_page, priority_guide_page,
    admin_dashboard_page, all_complaints_page, neg_esc_page, 
    analytics_page, staff_performance_page, resident_management_page
)

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),
    
    # Your Backend API endpoints
    path('api/', include('core.urls')), 
    
    # ─────────────────────────────────────────
    # BROWSER WEBSITE ROUTES
    # ─────────────────────────────────────────
    # Auth & General
    path('', index_page, name='index'),
    path('login/', login_page, name='login-page'),
    path('forgot-password/', forgot_password_page, name='forgot-password-page'),
    path('change-password/', change_password_page, name='change-password-page'),
    
    # Resident / User Pages
    path('dashboard/', user_dashboard_page, name='dashboard'),
    path('complaints/file/', register_complaint_page, name='file-complaint-page'),
    path('complaints/history/', my_complaints_page, name='my-complaints-page'),
    path('priority-guide/', priority_guide_page, name='priority-guide-page'),
    
    # Admin Pages
    path('admin-panel/', admin_dashboard_page, name='admin-dashboard-page'),
    path('admin-panel/all-complaints/', all_complaints_page, name='all-complaints'),
    path('admin-panel/escalations/', neg_esc_page, name='neg-esc-page'),
    path('admin-panel/analytics/', analytics_page, name='analytics'),
    path('admin-panel/staff-performance/', staff_performance_page, name='staff-performance-page'),
    path('admin-panel/residents/', resident_management_page, name='resident-manage-page'),
]

# Allow media file serving during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
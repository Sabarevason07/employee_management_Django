from django.urls import path
from Admin_Panel import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('',views.main,name="main"),
    path('home/',views.home,name="Home"),
    path("about/",views.about,name="About"),    
    path("login/",auth_views.LoginView.as_view(template_name='login.html'),name="Login"),
    path("logout/",views.logout,name="Logout"),
    path('register/',views.register,name="Register"),    
    path("profile/",views.profile,name="Profile"),
    path("add_employee/",views.add_employee,name="Add_Employee"),
    path("add/",views.add,name="add"),
    path("view/<int:id>/",views.view,name="view"),
    path("update/<int:id>/",views.update,name="update"),
    path("delete/<int:id>/",views.delete,name="delete"),
    path("dashboard/",views.dashboard,name="Dashboard"),
    path("update_user/<int:id>/",views.update_user,name="update_user"),
    path("delete_user/<int:id>/",views.delete_user,name="delete_user"),

    path('apply-leave/', views.apply_leave, name='apply_leave'),  # For employee
    path('leave-status/', views.leave_status, name='leave_status'),  # Employee checks status
    path('manage-leave-requests/', views.manage_leave_requests, name='manage_leave_requests'),  # Admin views leave requests
    path('approve-reject-leave/<int:leave_id>/<str:action>/', views.approve_reject_leave, name='approve_reject_leave'),
    path('attendance/', views.attendance_view, name='attendance'), 
      
    path('assign-task/', views.assign_task, name='assign_task'),
    path('tasks/', views.task_list, name='task_list'),
    
    path('award-wages/', views.award_wages, name='award_wages'),
    path('view-monthly-wages/', views.view_monthly_wages, name='view_monthly_wages'),
    
    path('send_request/', views.send_request, name='send_request'),
    path('notifications/', views.notification, name='notify'),

     path('qr-page/<int:employee_id>/', views.generate_qr_code, name='qr_page'),
     path('visual/', views.visual, name='visual'),

    path('feedback/', views.employee_feedback, name='employee_feedback'),
    path('feedback list/', views.feedback_list, name='feedback_list'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

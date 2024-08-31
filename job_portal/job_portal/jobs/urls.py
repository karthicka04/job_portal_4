from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [

    path('signup/', views.signup_view, name='register'), 
    path('login/', views.custom_login, name='login'),  
   
    path('dashboard/', views.job_list_view, name='dashboard'),  
   
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'), 
    path('create_job/', views.add_job_view, name='create_job'), 
    path('register/', views.register_job_view, name='register_job_view'),
    path('jobs/', views.job_list_view, name='job_list_view'),

]
from django.shortcuts import render, redirect  
from .forms import SignUpForm , JobForm , CustomUserLoginForm
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Job 
from .models import CustomUser,JobRegisteredUsers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


CustomUser = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'jobs/signup.html', {'form': form})

def login_required_view(request):
    if request.user.is_authenticated:
        return True
    return False

@login_required
def register_job_view(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        
        job = get_object_or_404(Job, id=job_id)
        
      
        registered_user, created = JobRegisteredUsers.objects.get_or_create(user=request.user, job=job)
        
        if created:
          
            return "Successfully registered"
        else:
           
            return "Failed to register"
    
    return redirect('job_list_view')

def job_list_view(request):
     if not login_required_view(request):
        return redirect('login')
     jobs = Job.objects.all()
     return render(request, 'jobs/job_list.html', {'jobs': jobs})

def admin_dashboard_view(request):
    if not login_required_view(request):
        return redirect('login')
    
    if request.user.is_superuser:
        section = request.GET.get('section', 'user_details')  # Default to 'user_details'
        
        if section == 'applicant_details':
            registered_users = JobRegisteredUsers.objects.all()
            return render(request, 'jobs/admin_dashboard.html', {'registered_users': registered_users, 'section': section})
        else:
            users = CustomUser.objects.all()
            return render(request, 'jobs/admin_dashboard.html', {'users': users, 'section': section})
    
    return redirect('login')




def register_job_view(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        
        # Retrieve the job object; if not found, raise a 404 error
        job = get_object_or_404(Job, id=job_id)
        
        # Check if the user is already registered for the job
        registered_user, created = JobRegisteredUsers.objects.get_or_create(user=request.user, job=job)
        
        if created:
            # User successfully registered for the job
            messages.success(request, f"You have successfully registered for the job: {job.role} at {job.company_name}.")
        else:
            # User was already registered for the job
            messages.warning(request, f"You are already registered for the job: {job.role} at {job.company_name}.")
    
    # Redirect back to the job list or refresh the page
    return redirect('job_list_view')


def add_job_view(request):
    if not login_required_view(request):
        return redirect('login')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'form': form})
def success_view(request):
    return render(request, 'jobs/success.html')

def custom_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:  
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
    else:
        form = CustomUserLoginForm()
    return render(request, 'jobs/login.html', {'form': form})
def home(request):
    return render(request, 'home.html')

def custom_logout(request):
    logout(request) 
    return redirect('login')
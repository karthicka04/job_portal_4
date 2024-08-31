from django import forms
from .models import CustomUser
from .models import Job
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'domain', 'is_experienced', 'resume']
        widgets = {
            'password': forms.PasswordInput(),
        }
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company_name', 'location', 'role', 'average_package', 'is_for_experienced']



    # Optionally customize the form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example customization: Add a widget for ForeignKey field
    
class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
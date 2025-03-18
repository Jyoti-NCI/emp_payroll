from django import forms
from django.contrib.auth.models import User
from .models import Employee
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employeeid', 'employeename', 'email', 'DOB', 'phone', 'base_salary', 'bonus', 'deductions', 'salary', 'image']
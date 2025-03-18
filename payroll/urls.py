"""
URL configuration for the emp_payroll app.

This module defines the URL patterns and routes for the emp_payroll app.
"""
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from payroll.forms import CustomLoginForm
app_name = 'payroll'
urlpatterns=[
    path("login/", LoginView.as_view(template_name="registration/login.html", form_class=CustomLoginForm), name="login"),
    path("", views.allemployees, name="allemployees"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("allemployees/", views.allemployees, name="allemployees"),
    path("singleemployee/<int:empid>/", views.singleemployee, name="singleemployee"),
    path("addemployee/", views.addemployee, name="addemployee"),
    path("deleteemployee/<int:empid>/", views.deleteemployee, name="deleteemployee"),
    path("updateemployee/<int:empid>/", views.updateemployee, name="updateemployee"),
    path("doupdateemployee/<int:empid>/", views.doupdateemployee, name="doupdateemployee")
]

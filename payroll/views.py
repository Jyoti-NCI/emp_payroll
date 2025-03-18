from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from datetime import datetime
from django.shortcuts import get_object_or_404
from . validators import *
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import logging
from django.conf import settings
from .aws_utils import upload_image_to_s3, send_sns_notification, log_to_cloudwatch
from django.contrib import messages
from django.http import JsonResponse


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("payroll:login")  # Redirect to login page upon success
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")  # Display friendly messages

    form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})
# View to log in a user
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("payroll:allemployees")
    else:
        form = UserLoginForm()
    return render(request, "registration/login.html", {"form": form})

# View to log out a user
def user_logout(request):
    logout(request)
    return redirect("payroll:login")


# Views to display all employees.
@login_required
def allemployees(request):
    if request.user.is_superuser:
        emp = Employee.objects.all()
    else:
        emp = Employee.objects.filter(added_by=request.user)
    return render(request, "payroll/allemployees.html", {"allemployees": emp})
# view to display a single employee
def singleemployee(request, empid):
    return render(request, "payroll/singleemployee.html")
#view to add employee
@login_required
def addemployee(request):
    if request.method == "POST":
        employeeid = request.POST.get('employeeid')
        employeename = request.POST.get('employeename')
        employeeemail = request.POST.get('employeeemail')
         # New: Check for duplicate email
        if Employee.objects.filter(email=employeeemail).exists():
            return HttpResponse("Employee with this email already exists.", status=400)
        employeeDOB = request.POST.get('employeeDOB')
        employeephone = request.POST.get('employeephone')
        base_salary = request.POST.get('baseSalary')
        bonus = request.POST.get('bonus')
        deductions = request.POST.get('deductions')
        salary = request.POST.get('employeesalary')

        e = Employee()
        e.employeeid = employeeid
        e.employeename = employeename
        e.email = employeeemail

        # convert DOB to proper Date format
        if employeeDOB:
            try:
                e.DOB = datetime.strptime(employeeDOB, "%Y-%m-%d").date()
            except ValueError:
                return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)

        e.phone = employeephone
        # Convert salary to float if provided
        if salary:
            try:
                e.salary = float(salary)
            except ValueError:
                return HttpResponse("Invalid salary format. Enter a numeric value.", status=400)
            
        # Handle image upload
        #image_file = request.FILES.get('image')
        #if image_file:
           # e.image = image_file
           
        # Upload Image to S3
        image_file = request.FILES.get("image")
        if image_file:
            s3_url = upload_image_to_s3(image_file)
            if s3_url:
                e.image = s3_url
                
        e.added_by=request.user
        e.save()
         # Send SNS notification
        send_sns_notification(f"New employee added: {employeename}")

        # Log event to CloudWatch
        log_to_cloudwatch(f"Employee {employeename} added.")

        return redirect("payroll:allemployees")

    return render(request, "payroll/addemployee.html")

#View to delete employee
@login_required
def deleteemployee(request, empid):
    e = Employee.objects.get(pk=empid)
    # Check if the logged-in user is the one who added the employee or is an admin
    if request.user != e.added_by and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this employee.")
        return redirect("payroll:allemployees")
    e.delete()
     # Log event to CloudWatch
    log_to_cloudwatch(f"Employee {e.employeename} deleted.")
    return redirect("payroll:allemployees")

#view to update employee
@login_required
def updateemployee(request, empid):
    e = get_object_or_404(Employee, pk=empid)
    # Check if the logged-in user is the one who added the employee or is an admin
    if request.user != e.added_by and not request.user.is_superuser:
        messages.error(request, "You do not have permission to update this employee.")
        return redirect("payroll:allemployees")
    return render(request, "payroll/updateemployee.html", {"singleemp": e})
@login_required
def doupdateemployee(request, empid):
    if request.method == "POST":
        emp = get_object_or_404(Employee, pk=empid)  # Fetch employee safely 
        # Check if the logged-in user is the one who added the employee or is an admin
        if request.user != emp.added_by and not request.user.is_superuser:
            messages.error(request, "You do not have permission to update this employee.")
            return redirect("payroll:allemployees")
        # Proceed with the update logic    
        updatedemployeeid = request.POST.get('employeeid')
        updatedemployeename = request.POST.get('employeename')
        updatedemployeeemail = request.POST.get('employeeemail')
        updatedemployeedob = request.POST.get('employeeDOB', '').strip()  # Ensure it's not empty
        updatedemployeephone = request.POST.get('employeephone')
        updated_base_salary = request.POST.get('baseSalary')
        updated_bonus = request.POST.get('bonus')
        updated_deductions = request.POST.get('deductions')
        updatedemployeesalary = request.POST.get('employeesalary')
         
    
        # Convert DOB to correct format
        if updatedemployeedob:  # Only update if a new DOB is provided
            try:
                emp.DOB = datetime.strptime(updatedemployeedob, "%Y-%m-%d").date()
            except ValueError:
                return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)

        # Update other fields
        emp.employeeid = updatedemployeeid
        emp.employeename = updatedemployeename
        emp.email = updatedemployeeemail
        emp.DOB = datetime.strptime(updatedemployeedob, "%Y-%m-%d").date()
        emp.phone = updatedemployeephone
       # Validate and update salary fields
        try:
            if updated_base_salary:
                emp.base_salary = float(updated_base_salary)
            if updated_bonus:
                emp.bonus = float(updated_bonus)
            if updated_deductions:
                emp.deductions = float(updated_deductions)
            # Use the computed total salary from the form or recalc to ensure consistency
            if updatedemployeesalary:
                emp.salary = float(updatedemployeesalary)
            else:
                emp.salary = emp.base_salary + emp.bonus - emp.deductions
        except ValueError:
            return HttpResponse("Invalid numeric format in salary fields.", status=400)
        
        
        # Upload new image to S3
        image_file = request.FILES.get("image")
        if image_file:
            s3_url = upload_image_to_s3(image_file)
            if s3_url:
                emp.image = s3_url
        emp.save()
         # Log update event to CloudWatch
        log_to_cloudwatch(f"Employee {updatedemployeename} updated.")
        
        return redirect("payroll:allemployees")
    return HttpResponse("Invalid request method", status=405)

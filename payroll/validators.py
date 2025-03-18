#this is a library which contains all validation logic for user input
from datetime import datetime
import re

def validate_employee_id(employee_id):
    #Validates that the employee ID is alphanumeric and 3-20 characters long.
    if not re.match(r"^[A-Za-z0-9]{3,20}$", employee_id):
        return "Employee ID must be alphanumeric and 3-20 characters long."
    return None

def validate_name(name):
    #Validates that the name contains only letters and spaces, and is 3-50 characters long.
    if not re.match(r"^[A-Za-z ]{3,50}$", name):
        return "Name must be alphabetic and 3-50 characters long."
    return None

def validate_email(email):
    #Validates that the email follows a correct format.
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return "Please enter a valid email address (e.g., user@example.com)."
    return None

def validate_phone(phone):
    #Validates that the phone number contains exactly 10 digits.
    if not re.match(r"^[0-9]{10}$", phone):
        return "Phone number must be exactly 10 digits."
    return None

def validate_dob(dob):
    #Validates that the employee is at least 22 years old.
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
        today = datetime.today().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 22:
            return "Employee must be at least 22 years old."
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."
    return None

def validate_salary(base_salary, bonus, deductions):
    #Validates that the base salary is at least 1000 and other values are non-negative.
    try:
        base_salary = float(base_salary)
        bonus = float(bonus) if bonus else 0
        deductions = float(deductions) if deductions else 0

        if base_salary < 1000:
            return "Base salary must be at least 1000."
        if bonus < 0 or deductions < 0:
            return "Bonus and deductions must be non-negative."

        total_salary = base_salary + bonus - deductions
        if total_salary <= 0:
            return "Total salary must be greater than zero."
    except ValueError:
        return "Salary fields must be numeric values."
    
    return None
  #Validates that the salary is numeric and non-negative.
#def validate_salary(salary):
    try:
        salary = float(salary)
        if salary < 0:
            return "Salary must be a non-negative value."
    except ValueError:
        return "Salary must be a numeric value."
    return None


"""
Models for the payroll app.
This module defines the database models for managing employee payroll.
"""
from django.db import models
from django.contrib.auth.models import User
"""
Represents an employee in the payroll system.
"""
class Employee(models.Model):
    employeeid             = models.CharField(max_length=20, unique=False)
    employeename           = models.CharField(max_length=50)
    email                  = models.CharField(max_length=50, unique=True)
    DOB                    = models.DateField(null=True, blank=True)
    phone                  = models.CharField(max_length=50)
    base_salary            = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bonus                  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    deductions             = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    salary                 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image                  = models.URLField(null=True, blank=True)
    added_by               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employees')
   # image = models.ImageField(upload_to='employees/', null=True, blank=True)
    """
    Returns a string representation of the employee.
    """
    def __str__(self):
        return self.employeename
    @property
    def is_post_production_completed(self):
        return self.salary > 0
        
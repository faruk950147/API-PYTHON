from django.db import models
from datetime import date

class Employee(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    dob = models.DateField(default=date.today)
    phone = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(unique=True)
    
    gender = models.CharField(max_length=10)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.TextField(default="Not provided")
    department = models.CharField(max_length=100)
    
    status = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = "employees"
        ordering = ["-created_at"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.name
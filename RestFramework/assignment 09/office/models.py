from django.db import models
from datetime import date


class Company(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    address = models.TextField(default="Not provided")
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    website = models.URLField(default="Not provided")
    industry = models.CharField(max_length=100, default="Not provided")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = "companies"
        ordering = ["-created_at"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Department(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(default="Not provided")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = "departments"
        ordering = ["-created_at"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.name} - {self.company.name}"


class Employee(models.Model):
    STATUS = (("active", "Active"),
              ("inactive", "Inactive"),
              ("terminated", "Terminated")
            )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")

    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField(default=date.today)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="active",
        db_index=True
    )

    address = models.TextField(default="Not provided")

    date_of_birth = models.DateField(default=date.today)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = "employees"
        ordering = ["-created_at"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.name} - {self.company.name}"
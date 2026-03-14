from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class CommonMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Admission(CommonMixin):
    QUALIFICATION_CHOICES = (
        ('SSC', 'SSC'),
        ('HSC', 'HSC'),
        ('BSc', 'BSc'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    DEPARTMENT_CHOICES = (
        ('CSE', 'CSE'),
        ('EEE', 'EEE'),
        ('BBA', 'BBA'),
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    dob = models.DateField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    qualification = models.CharField(max_length=10, choices=QUALIFICATION_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def clean(self):
        """Custom validation logic"""
        today = date.today()

        # Age validation (minimum 15)
        if self.dob:
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            if age < 15:
                raise ValidationError({'dob': 'Admission requires minimum age 15'})

        # GPA validation (minimum 3.50)
        if self.gpa < 3.50:
            raise ValidationError({'gpa': 'GPA must be at least 3.50'})

        # Qualification validation (minimum HSC)
        if self.qualification == 'SSC':
            raise ValidationError({'qualification': 'Minimum qualification is HSC'})

    def save(self, *args, **kwargs):
        # Run full validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = "admission"
        ordering = ["-created_at"]
        verbose_name = "Admission"
        verbose_name_plural = "Admission"

    def __str__(self):
        return f'{self.name} | {self.dob} | GPA: {self.gpa} | {self.qualification} | {self.gender} | {self.department} | {self.status}'

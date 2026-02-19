from django.db import models

# Create your models here.

class CommonMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = '01 - Admissions'

    def __str__(self):
        return f'{self.name} | {self.dob} | GPA: {self.gpa} | {self.qualification} | {self.gender} | {self.department} | {self.status}'

    def clean(self):
        if self.gpa < 3.50:
            raise ValidationError({'gpa': 'GPA must be at least 3.50'})

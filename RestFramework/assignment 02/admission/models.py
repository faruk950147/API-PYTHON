from django.db import models

class Registration(models.Model):
    name = models.CharField(max_length=150)
    roll = models.IntegerField()
    cgpa = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

    class Meta:
        ordering = ['id']
        verbose_name_plural = '01 - Admissions'

    def __str__(self):
        return f"{self.name} ({self.roll})"

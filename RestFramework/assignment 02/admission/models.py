from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=150)
    roll = models.IntegerField()
    cgpa = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Student"
        ordering = ["-created_at"]
        verbose_name = "Student"
        verbose_name_plural = "Student"

    def __str__(self):
        return f"{self.name} ({self.roll})"

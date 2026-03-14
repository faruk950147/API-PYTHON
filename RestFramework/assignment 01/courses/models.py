from django.db import models

class Courses(models.Model):
    name = models.CharField(max_length=150, unique=True)
    trainer = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Courses"
        ordering = ["-created_at"]
        verbose_name = "Courses"
        verbose_name_plural = "Courses"
    def __str__(self):
        return self.name
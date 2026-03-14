from django.db import models

class Courses(models.Model):
    name = models.CharField(max_length=150, unique=True)
    trainer = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    
    class Meta:
        db

    def __str__(self):
        return self.name
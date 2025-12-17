from django.db import models

class Addmission(models.Model):
    name = models.CharField(max_length=150)
    roll = models.IntegerField()
    cgpa = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.roll})"

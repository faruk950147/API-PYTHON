from django.db import models

class Post(models.Model):
    author = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "post"
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        
    def __str__(self):
        return self.title


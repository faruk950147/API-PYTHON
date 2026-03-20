from django.contrib import admin
from official.models import Post


# ==============================
# Post Admin
# ==============================
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'tags', 'title', 'content', 'created_at', 'updated_at']
    search_fields = ['title', 'content', ]
    list_filter = ['author', 'tags', 'created_at']


admin.site.register(Post, PostAdmin)



from rest_framework import serializers
from official.models import Post



class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'tags', 'title', 'content', 'created_at', 'updated_at']
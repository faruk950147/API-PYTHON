from rest_framework import serializers
from datetime import datetime


class CoursesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    trainer = serializers.CharField(max_length=150)
    duration = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        validated_data["created_at"] = datetime.now()
        validated_data["updated_at"] = datetime.now()
        return validated_data

    def update(self, instance, validated_data):
        instance["name"] = validated_data.get("name", instance["name"])
        instance["trainer"] = validated_data.get("trainer", instance["trainer"])
        instance["duration"] = validated_data.get("duration", instance["duration"])
        instance["updated_at"] = datetime.now()
        return instance
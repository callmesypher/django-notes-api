from rest_framework import serializers
from .models import Note
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteSerializer(serializers.ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "shared_with",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_shared_with(self, value):
        user = self.context["request"].user

        if user in value:
            raise serializers.ValidationError(
                "You cannot share a note with yourself."
            )

        return value
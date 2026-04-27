from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_notes")
    shared_with = models.ManyToManyField(User, blank=True, related_name="shared_notes")
    
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["owner", "-created_at"]
                )
        ]
        constraints= [
            models.UniqueConstraint(
                fields= ["owner", "title"],
                name= "unique_note_title_per_user"
            )
        ]

    def __str__(self):
        return f"{self.title or 'Untitled'} by {self.owner.username}"

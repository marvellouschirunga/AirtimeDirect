from django.db import models
from django.contrib.auth.models import AbstractUser  # Import Django's customizable user model

# Create your models here.
class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Adds additional fields specific to this project, such as name, email, bio, avatar, and online status.
    """

    STATUS = (
        ('Technology Missionary', 'Technology Missionary'),  # Peer Mentor
        ('Mission President', 'Mission President'),  # Peer Mentor Support Agent
        ('Finance Secretary', 'Finance Secretary')  # Support Manager
    )
    name = models.CharField(max_length=200, null=True)  # Full name of the user
    email = models.EmailField(unique=True, null=True)  # User's unique email, which serves as the username
    avatar = models.ImageField(null=True, default="avatar.svg")  # Profile image or avatar for the user

    # Override the default username field to use email for authentication
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  # No extra required fields apart from email

    def __str__(self):
        """
        String representation of the user object.
        Returns the user's name if available, otherwise the user's email.
        """
        return self.name if self.name else self.email
    
class AirtimeRequest(models.Model):
    phone_number = models.CharField(max_length=15)
    owner_name = models.CharField(max_length=100)
    data_bundle = models.CharField(max_length=50)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending')
    updated = models.DateTimeField(auto_now=True)  # Automatically updates when the airtime request  is updated
    created = models.DateTimeField(auto_now_add=True)  # Automatically sets when the airtime request is created

class Meta:
    """
    Meta options to specify the ordering of the rooms.
    Rooms are ordered by the most recently updated and created.
    """
    ordering = ['-updated', '-created']  # Order rooms by most recent updates and creations

def __str__(self):
    """
    String representation of the room object.
    Returns the name of the room.
    """
    return self.name

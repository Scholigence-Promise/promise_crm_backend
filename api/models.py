from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
from django.db import models
from django.contrib.auth.models import User

#creation of model for Roles:
class Role(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Superadmin'),
        ('general manager', 'General manager'),
        ('operations manager', 'Operations manager'),
        ('department head','Department head'),
        ('underwriter','Underwriter'),
        ('sales manager','Sales manager'),
        ('telecallers','Telecallers'),
        ('customers','Customers')
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
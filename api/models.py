#creation of model for Roles:
from django.db import models
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
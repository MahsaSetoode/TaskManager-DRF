from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


class Task(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    title = models.CharField(
            max_length=150,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    description = models.TextField(null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title

    # order of showing items in admin or extra
    class Meta:
        ordering = ['created_at']
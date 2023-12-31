import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from payments.models import Payment

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    def profile_image_path(instance, filename):
        return f'profile/{instance.email}/{filename}'
    image = ProcessedImageField(upload_to=profile_image_path, blank=True, null=True, processors=[ResizeToFill(100,100)])
    subscription = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriber')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def delete(self, *args, **kwargs):
        if self.image:
            path = self.image.path
            if os.path.isfile(path):
                os.remove(path)
        super().delete(*args, **kwargs)
    
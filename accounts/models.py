import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from payments.models import Payment

# Create your models here.
class User(AbstractUser):
    email = models.EmailField()
    def profile_image_path(instance, filename):
        return f'profile/{instance.email}/{filename}'
    image = ProcessedImageField(upload_to=profile_image_path, blank=True, null=True, processors=[ResizeToFill(100,100)])
    pay_stutus = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="user_pay_status")

    def delete(self, *args, **kwargs):
        if self.image:
            path = self.image.path
            if os.path.isfile(path):
                os.remove(path)
        if self.background_image:
            path = self.background_image.path
            if os.path.isfile(path):
                os.remove(path)
        super().delete(*args, **kwargs)
    
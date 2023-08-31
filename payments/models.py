from django.db import models
from django.conf import settings

# Create your models here.

class Subscription(models.Model):
    DURATION_CHOICES = (('1MF', '첫 달 무료'), ('1M', '1 개월'), ('3M', '3 개월'), ('6M', '6 개월'), ('1Y', '1 년'),)
    title = models.CharField(max_length=50, choices=DURATION_CHOICES)
    price = models.IntegerField(default=0)
    months = models.IntegerField(default=1) 

    def __str__(self):
        return self.title


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE) 
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


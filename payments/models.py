from django.db import models
from django.conf import settings

# Create your models here.
class Prices(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    period = models.CharField(max_length=15)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.ForeignKey(Prices, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
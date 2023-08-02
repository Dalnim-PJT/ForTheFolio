from django.shortcuts import render
from .models import Subscription

# Create your views here.
def index(request):
    subscriptions = Subscription.objects.all()
    context = {
        'subscriptions': subscriptions
    }

    return render(request, 'payments/index.html', context)
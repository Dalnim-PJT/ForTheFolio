from django.urls import reverse_lazy
import json

def navbar(request):
    navbar_items = [
        {"name": "템플릿", "url": str(reverse_lazy('portfolios:index')), "class": "portfolio"},
        {"name": "요금", "url": str(reverse_lazy('payments:index')), "class": "payments"},
    ]
    navbar_items_json = json.dumps(navbar_items)
    return {'navbar_items': navbar_items_json}


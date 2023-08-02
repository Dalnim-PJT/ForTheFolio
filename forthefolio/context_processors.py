from django.urls import reverse_lazy
import json

def navbar(request):
    navbar_items = [
        {"name": "템플릿", "url": str(reverse_lazy('portfolios:index')), "class": "portfolio"},
        {"name": "요금", "url": str(reverse_lazy('payments:index')), "class": "payments"},
    ]
    navbar_items_json = json.dumps(navbar_items)
    return {'navbar_items': navbar_items_json}

# 앱네임을 사용하기 위해 reverse를 사용해야하나, reverse는 재귀호출 에러
# reverse_lazy는 JSON에 __proxy__ 오브젝트를 직렬화하려고 하는 문제 : str()사용하여 해결됨.
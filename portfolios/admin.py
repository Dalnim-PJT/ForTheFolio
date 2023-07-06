from django.contrib import admin
from .models import TechStack, P_templates, Portfolios, Career, Pjts, Pjtimages

# Register your models here.

admin.site.register(TechStack)
admin.site.register(P_templates)
admin.site.register(Portfolios)
admin.site.register(Career)
admin.site.register(Pjts)
admin.site.register(Pjtimages)

from django.apps import apps
from django.contrib import admin

# Auto Register all models
app = apps.get_app_config("quickstart")

for model in app.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

# Register your models here manually
# from .models import User
# admin.site.register(User)

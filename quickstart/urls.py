# URL Configuration for the new app
from django.urls import path, include
from rest_framework import routers

from . import views

route = routers.DefaultRouter()
route.register(r"person", views.PersonViewSet, basename="PersonViewSet")

urlpatterns = [path("", include(route.urls))]

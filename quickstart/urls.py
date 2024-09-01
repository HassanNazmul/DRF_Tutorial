# URL Configuration for the new app
from django.urls import path

from . import views

urlpatterns = [
    # GET all the data from the Person model
    path('person/', views.PersonAPIView.as_view(), name="person-list"),
    # GET Person by ID
    path('person/<int:id>/', views.PersonAPIView.as_view(), name="person"),
]

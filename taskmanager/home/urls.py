from django.urls import path
from . import views
# from django.contrib.auth import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]

from django.urls import path
from . import views


urlpatterns = [
    # api endpoints
    path('', views.TaskListCreateApi.as_view(), name='task_list_create_api'),
    path('details/<int:pk>/', views.TaskDetailApi.as_view(), name='task_details_api'),
]
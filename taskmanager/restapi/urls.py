from django.urls import path
from . import views


urlpatterns = [
    # api endpoints
    path('tasks/', views.TaskListCreateApi.as_view(), name='task_list_create_api'),
    path('task/<int:pk>/', views.TaskDetailApi.as_view(), name='task_detail_api'),
]

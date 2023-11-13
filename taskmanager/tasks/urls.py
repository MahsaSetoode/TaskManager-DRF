from django.urls import path
from . import views

# app_name='tasks'
urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list_create'),
    path('details/<int:pk>/', views.TaskDetail.as_view(), name='task_details'),
    path('edit/<int:pk>/', views.TaskEdit.as_view(), name='task_edit'),
    path('delete/<int:pk>/', views.TaskDelete.as_view(), name='task_delete'),
]

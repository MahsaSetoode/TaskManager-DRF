from django.urls import path
from . import views


urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list_create'),
    path('detail/<int:pk>/', views.TaskDetail.as_view(), name='task_details'),
    path('edit/<int:pk>/', views.TaskEdit.as_view(), name='task_edit'),
    path('delete/<int:pk>/', views.TaskDelete.as_view(), name='task_delete'),
]

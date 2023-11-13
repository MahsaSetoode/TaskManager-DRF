from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from tasks.models import Task
from .serializers import TaskSerializer, CreateTaskSerializer, EditTaskSerializer


# using serializer and django rest 
class TaskListCreateApi(LoginRequiredMixin, APIView):
  
    # tasks list
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)
    
    # create task
    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if not self.request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},status=status.HTTP_401_UNAUTHORIZED)
        # print(self.request.user)
        # print(serializer.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailApi(LoginRequiredMixin, APIView):
    # task detail
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    # deserialize and update
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = EditTaskSerializer(task, data=request.data,partial = True)
        if self.request.user != task.owner:
            return Response({'detail': 'Your not the owner.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if self.request.user != task.owner:
            return Response({'detail': 'Your not the owner.'}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

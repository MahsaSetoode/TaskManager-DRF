from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from tasks.models import Task
from .serializers import TaskSerializer, CreateTaskSerializer, EditTaskSerializer
from .forms import TaskCreateForm, TaskEditForm



class TaskList(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_list.html'

    # tasks list
    def get(self, request):
        # handles searching
        search_item =  request.GET.get("search", False)
        if search_item :
            # if user searched anything
            # Q => query expression
            tasks = Task.objects.filter(Q(title__icontains=search_item) | Q(description__icontains=search_item))
        else :
            tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response({'task_list': serializer.data, 'search':search_item})
        # return render(request, 'tasks/task_list.html', {'task_list': serializer.data})
    
    # create task
    def post(self, request):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            # Save the task
            task = form.save(commit=False)
            task.owner = self.request.user
            task.save()
            return redirect('task_list_create')
        tasks = Task.objects.all()
        return Response({'task_list': tasks, "form":form})


class TaskDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_detail.html'
    # task detail
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response({'task': serializer.data, 'owner': task.owner})
    


class TaskEdit(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_form.html'
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        if task.owner != request.user:
            return redirect('task_list_create')
        return Response({'task': serializer.data})
    
    # deserialize and update
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list_create')
        return Response({'task': task, "form":form})
    
class TaskDelete(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_delete_confirm.html'
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        if task.owner != request.user:
            return redirect('task_list_create')
        return Response({'task': serializer.data})
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('task_list_create')
    
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(TaskDelete, self).get_queryset()
        return qs.filter(owner=self.request.user)


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
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if self.request.user != task.owner:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

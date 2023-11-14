from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskList(TestCase):
    def setUp(self):
        # create a user for authentication
        self.user = User.objects.create_user(
            username='mahsa',
            password='mahsa'
        )

        # create some tasks for test
        Task.objects.create(title='Task 1', description='Description 1', owner=self.user)
        Task.objects.create(title='Task 2', description='Description 2', owner=self.user)
        Task.objects.create(title='Task 3', description='Description 3', owner=self.user)

    def test_task_list_view(self):
        username_='mahsa'
        password_='mahsa'

        # create and login test client
        self.client.login(username=username_, password=password_)
        # access
        url = reverse('task_list_create')
        
        # create get request
        response = self.client.get(url)

        # check response
        self.assertEqual(response.status_code, 200)


    # testing search
    def test_task_search(self):
        username_='mahsa'
        password_='mahsa'

        self.client.login(username=username_, password=password_)
        url = reverse('task_list_create')
        response = self.client.get(url, {'search': 'Task'})
        self.assertEqual(response.status_code, 200)

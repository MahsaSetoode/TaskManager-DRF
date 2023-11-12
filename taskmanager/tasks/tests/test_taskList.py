from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskList(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='mahsa',
            password='mahsa12345'
        )

        # Create some tasks for testing
        Task.objects.create(title='Task 1', description='Description 1', owner=self.user)
        Task.objects.create(title='Task 2', description='Description 2', owner=self.user)
        Task.objects.create(title='Task 3', description='Description 3', owner=self.user)

    def test_task_list_view(self):
        username_='mahsa'
        password_='mahsa12345'

        # Create a test client and log in the user
        self.client.login(username=username_, password=password_)

        # Access the task_list_create view
        url = reverse('task_list_create')
        
        # Use the test client to make the request
        response = self.client.get(url)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the task titles
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
        self.assertContains(response, 'Task 3')

    def test_task_search(self):
        username_='mahsa'
        password_='mahsa12345'

        # Create a test client and log in the user
        self.client.login(username=username_, password=password_)

        url = reverse('task_list_create')
        
        # Use the test client to make the request with search parameters
        response = self.client.get(url, {'search': 'Task 1'})

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the searched task
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 3')
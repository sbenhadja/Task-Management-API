from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User
from .models import Task
from .serializers import TaskSerializer
from rest_framework_simplejwt.tokens import AccessToken

# Create your tests here.
class TaskListByUserTestCase(APITestCase):

    def setUp(self):
        # Create the user
        self.user = User.objects.create(email='testuser@mail.com', password="test", is_active=True, username="testuser", first_name="", last_name="")
        
        # Create a token for the user
        self.token = AccessToken.for_user(self.user)
        
        # Check user and token creation
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(self.token)
                
        # Create tasks for the user
        self.task = Task.objects.create(title='Task 1', description='Description 1', due_date='2024-03-14T12:00:00Z', user=self.user)
        Task.objects.create(title='Task 2', description='Description 2', due_date='2024-03-14 13:00:00+00:00', user=self.user)

    def test_list_task_by_user(self):
        # Set the token in the request headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Make a GET request
        url = reverse('list-tasks-by-user')
        response = self.client.get(url)

        # Check the response status is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the serialized data
        tasks = Task.objects.all().order_by('due_date')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_edit_task_by_user(self):
        # Set the token in the request headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Data to be updated
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'due_date': '2024-03-15 13:00:00+00:00'
        }

        url = reverse('update-task', kwargs={'pk': self.task.id})

        # Make a PUT request
        response = self.client.put(url, updated_data, format='json')

        # Check the response status 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the updated data
        self.task.refresh_from_db()

        # Check the updated data
        self.assertEqual(self.task.title, updated_data['title'])
        self.assertEqual(self.task.description, updated_data['description'])
        self.assertEqual(str(self.task.due_date), updated_data['due_date'])


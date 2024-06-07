from operator import index
from urllib import response
from xml.etree.ElementTree import tostring
from django.core.paginator import Paginator,EmptyPage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from task.serializers import TaskSerializer
from task.models import Task
from rest_framework.permissions import IsAuthenticated, IsAuthenticated

#Add task by the authenticated user
class AddTask(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        user = request.user
        data = request.data
        if (data.keys() >= {"title", "description", "due_date"}):
            data['user'] = user.id
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            response = serializer.errors[(list(serializer.errors.keys()))[0]][0]
            return Response({'error':response}, status = status.HTTP_400_BAD_REQUEST )
        return Response({"error": 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

#Update selected task by the authenticated user
class UpdateTask(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = TaskSerializer

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        taskData = request.data
        
        required_keys = {"title", "description", "due_date", "status"}
        if taskData.keys() & required_keys:
            
            def data_to_changes():
                #return a dictionary containing non-empty values from the given task data
                data_to_change = {key: value for key, value in taskData.items() if value != ''}
                return data_to_change

            try:
                task = Task.objects.get(id=pk, user=user)
                serializer = self.serializer(
                    instance=task, data=data_to_changes(), partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_200_OK)
                response = serializer.errors[(list(serializer.errors.keys()))[0]][0]
                return Response({'error':response}, status = status.HTTP_400_BAD_REQUEST)
            except Task.DoesNotExist:
                # no task matches the criteria
                 return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

#Delete selected task by the authenticated user
class DeleteTask(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, pk, format=None):
        user = request.user
        try:
            Task.objects.get(id=pk,user=user).delete()
        except Task.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({"reponse": "Deleted successfully"},status=status.HTTP_200_OK)

#Find one specific task by the authenticated user
class GetTask(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        user = request.user
        try:
            tasks = Task.objects.get(id=pk, user=user)
        except Task.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(tasks)
        return Response(serializer.data, status=status.HTTP_200_OK)

#List all tasks OR by Filter by the authenticated user
class ListTasksByUser(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        data = request.query_params
        filters = {key + '__exact': value for key, value in data.items() if value}
        tasks = Task.objects.filter(user=user, **filters).order_by('due_date')  

        if tasks.exists():
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

#List all tasks by the authenticated user by page number and number of tasks
class ListTasksPaginator(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, elmbypage, numpage, format=None):
        user = request.user
        tasks = Task.objects.filter(user=user).order_by('due_date')
        if tasks.exists():
            try:
                paginator = Paginator(tasks, elmbypage)
                page = paginator.page(numpage)
                serializer = TaskSerializer(page.object_list, many=True)
            except EmptyPage:
                return Response({'error': 'Page not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'elements':serializer.data,'nb_elements':paginator.count,'nb_pages':paginator.num_pages,'num_page':numpage,
                         'elm_by_page':elmbypage,'page_has_next':page.has_next(),'page_has_previous':page.has_previous()}, status=status.HTTP_200_OK)
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
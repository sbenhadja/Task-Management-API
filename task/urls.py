from django.urls import path
from task import views

urlpatterns = [
    path('tasks/add', views.AddTask.as_view(), name='add-task'),
    path('tasks/update/<uuid:pk>', views.UpdateTask.as_view(), name='update-task'),
    path('tasks/delete/<uuid:pk>', views.DeleteTask.as_view(), name='delete-task'),
    path('tasks/<uuid:pk>', views.GetTask.as_view(), name='get-task'),
    path('tasks', views.ListTasksByUser.as_view(), name='list-tasks-by-user'),
    path('tasks/<int:elmbypage>/<int:numpage>', views.ListTasksPaginator.as_view(), name='tasks-paginator'),
]
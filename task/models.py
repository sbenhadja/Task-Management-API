from enum import Enum
from django.db import models
import uuid

from core.models import User

# Create your models here.
class Status(Enum):
    COMPLETE = 'Complete'
    INCOMPLETE = 'Incomplete'

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateTimeField(blank=False, null=False)
    # create_on =  models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(status.name, status.value) for status in Status], default=Status.INCOMPLETE.name)

    class Meta:
        db_table = "task"



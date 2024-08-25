from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Notes section
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
        
    # For Removing Extra "s" from Notess
    class Meta:
        verbose_name = 'Notes'
        verbose_name_plural = 'Notes'


#Home_work Section
class Homework(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.subject


#Todo Section
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


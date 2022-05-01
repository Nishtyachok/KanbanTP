from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    details = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = (
            ('member_project', 'member project'),
        )

    def __str__(self):
        return self.name


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('owner',)


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = (
        ('T', 'To Do'),
        ('D', 'Doing'),
        ('I', 'In Test'),
        ('O', 'Done'),
    )
    status = models.CharField(max_length=1, choices=status_choices)
    start_time = models.DateField(null=True)
    end_time = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

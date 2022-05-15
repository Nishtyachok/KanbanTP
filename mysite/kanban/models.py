from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    details = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

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


class Row(models.Model):
    name = models.CharField(max_length=50,)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RowForm(ModelForm):

    class Meta:
        model = Row
        fields = '__all__'
        exclude = ('project',)
        labels = {
            'name': '',
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Введите название'}),
        }


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.ForeignKey(Row, on_delete=models.SET_NULL, null=True)
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('project', 'assigned_to', 'row', 'start_time')
        labels = {
            'name': 'Название задачи',
            'description': 'Описание',
            'end_time': 'Выполнить до',
        }
        # widgets = {
        #     'name': TextInput(attrs={'placeholder': 'Введите название'}),
        # }


class Team(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members')

    def __str__(self):
        return self.project.name
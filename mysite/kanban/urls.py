from django.urls import path
from .views import Projects, Tasks, DeleteProject, DeleteRow, DeleteTask, addMember

urlpatterns = [
    path('', Projects.as_view(), name='boards'),
    path('share/<key>', addMember, name='share'),
    path('<id>/deleteProject', DeleteProject.as_view(), name='delete board'),
    path('boards/<id>/<id_task>/deleteTask', DeleteTask.as_view(), name='delete task'),
    path('boards/<id>/<id_row>/deleteRow', DeleteRow.as_view(), name='delete row'),
    path('<id>', Tasks.as_view(), name='tasks'),
]


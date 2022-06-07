from django.urls import path
from .views import Projects, Tasks, deleteProject, deleteRow, deleteTask, addMember, deleteMember

urlpatterns = [
    path('', Projects.as_view(), name='boards'),
    path('share/<key>', addMember, name='share'),
    path('<id>/deleteProject', deleteProject, name='delete board'),
    path('<id>/<id_member>/deleteMember', deleteMember, name='delete member'),
    path('boards/<id>/<id_task>/deleteTask', deleteTask, name='delete task'),
    path('boards/<id>/<id_row>/deleteRow', deleteRow, name='delete row'),
    path('<id>', Tasks.as_view(), name='tasks'),
]


from django.urls import path
from .views import Projects, Task, DeleteProject

urlpatterns = [
    path('', Projects.as_view(), name='boards'),
    path('<id>/delete', DeleteProject.as_view(), name='tasks'),
]
from django.urls import path
from .views import Projects, Tasks, DeleteProject

urlpatterns = [
    path('', Projects.as_view(), name='boards'),
    path('<id>/delete', DeleteProject.as_view(), name='delete board'),
    path('<id>', Tasks.as_view(), name='tasks'),
]
from django.urls import path
from .views import Projects, Tasks

urlpatterns = [
    path('', Projects.as_view(), name='boards'),
    path('<id>', Tasks.as_view(), name='tasks'),
]
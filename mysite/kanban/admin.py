from django.contrib import admin
from .models import Project, Task, Row, Team

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Row)
admin.site.register(Team)
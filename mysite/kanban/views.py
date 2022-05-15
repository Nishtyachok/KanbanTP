from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Task, ProjectForm, RowForm, Row, TaskForm, Team
from guardian.shortcuts import get_objects_for_user, assign_perm
from django.core.paginator import Paginator


class Projects(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user
        user_projects = Project.objects.filter(team__members__id=user.id)

        paginator = Paginator(user_projects, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {"user": user,
                "projects": page_obj,
                'form': ProjectForm()
                }
        return render(request, 'boards.html', data)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user

        form = ProjectForm(request.POST)
        if form.is_valid():
            s_form = form.save(commit=False)
            s_form.owner = user
            s_form.save()

        return redirect('boards')


class DeleteProject(View):
    def get(self, request, id):
        try:
            proj = Project.objects.get(id=id)
        except:
            return redirect('boards')
        if request.user.id == proj.owner.id:
            proj.delete()
        return redirect('boards')


class Tasks(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect("/")
        proj = Project.objects.filter(id=id).first()
        user = request.user
        # users = User.objects.filter(Q(id__in=proj.get_members()) | Q(id=proj.owner.id))
        rows = Row.objects.filter(project_id=id)
        paginator = Paginator(rows, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {"user": user,
                "first": user.username[0],
                "tasks": proj.task_set.all(),
                'proj': proj,
                'rows': page_obj,
                "can_add": user == proj.owner,
                "row_form": RowForm(),
                "task_form": TaskForm(),
                }
        return render(request, 'tasks.html', data)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return redirect('/')
        if request.POST.get('row_add'):
            row_form = RowForm(request.POST)
            if row_form.is_valid():
                s_form = row_form.save(commit=False)
                s_form.project = Project.objects.filter(id=id).first()
                s_form.save()
        if request.POST.get('task_add'):
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                s_form = task_form.save(commit=False)
                s_form.project = Project.objects.filter(id=id).first()
                s_form.row = Row.objects.filter(id=request.POST.get('row_id')).first()
                s_form.assigned_to = request.user
                s_form.save()
        return redirect(f'/boards/{id}')



#
#
# class ManegeTasks(View):
#     def post(self, request, id):
#         if not request.user.is_authenticated:
#             response = JsonResponse({"error": "Invalid User"})
#             response.status_code = 403
#             return response
#
#         user = request.user
#
#         type = request.POST['type']
#         if type == 'edit_status':
#             task_id = request.POST['task_id']
#             status = request.POST['board_id']
#
#             task = Task.objects.filter(id=task_id).first()
#
#             if status in ['O', 'B', 'L'] or task.status in ['O', 'B', 'L']:
#                 if user == task.project.owner:
#                     task.status = status
#                     task.save()
#
#                 else:
#                     response = JsonResponse({"error": "You Do Not Have Permission"})
#                     response.status_code = 403
#                     return response
#             else:
#                 if user == task.assigned_to or user == task.project.owner:
#                     task.status = status
#                     if status == 'D':
#                         # task.start_time = datetime.datetime.today().date()
#                         pass
#                     task.save()
#                 else:
#                     response = JsonResponse({"error": "You Do Not Have Permission"})
#                     response.status_code = 403
#                     return response
#
#             response = JsonResponse({"message": "OK"})
#             response.status_code = 200
#             return response
#
#         if type == 'edit_end_time':
#
#             task_id = request.POST['task_id']
#             end_time = request.POST['new_end_time']
#
#             task = Task.objects.filter(id=task_id).first()
#
#             if user == task.project.owner:
#                 task.end_time = end_time
#                 task.save()
#
#                 response = JsonResponse({"message": "OK"})
#                 response.status_code = 200
#                 return response
#
#             else:
#                 response = JsonResponse({"error": "You Do Not Have Permission"})
#                 response.status_code = 403
#                 return response

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Task, ProjectForm
from guardian.shortcuts import get_objects_for_user, assign_perm
from django.core.paginator import Paginator


class Projects(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user
        try:
            user_projects = get_objects_for_user(user,
                                                 perms=['kanban.member_project', ],
                                                 klass=Project)
        except:
            user_projects = []
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
            assign_perm('Project.member_project', user, Project.objects.get(id=s_form.id))

        return redirect('boards')


class DeleteProject(View):
    def post(self, request, id):
        Project.objects.filter(id=id).delete()
        response = JsonResponse({"message": "OK"})
        response.status_code = 200
        return response


# # class Tasks(View):
#     def get(self, request, id):
#         if not request.user.is_authenticated:
#             return redirect("signIn")
#
#         proj = Project.objects.filter(id=id).first()
#         user = request.user
#         users = User.objects.filter(Q(id__in=proj.get_members()) | Q(id=proj.owner.id))
#         data = {"user": user,
#                 "first": user.username[0],
#                 "other_users": users,
#                 "tasks": proj.task_set.all(),
#                 'proj': proj,
#                 "can_add": user == proj.owner
#                 }
#         return render(request, 'tasks.html', data)
#
#     def post(self, request, id):
#         if not request.user.is_authenticated:
#             return redirect('signIn')
#
#         name = request.POST['name']
#         description = request.POST['desc']
#         assigned_to = request.POST['users']
#         status = 'T'
#         end_time = request.POST['date']
#
#         task = Task(name=name, description=description, assigned_to_id=assigned_to, status=status,
#                     end_time=end_time, project_id=id)
#         task.save()
#
#         return redirect('tasks', id=id)
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

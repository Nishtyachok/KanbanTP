
from django.shortcuts import render, redirect
from django.views import View
from .models import Project, Task, ProjectForm, RowForm, Row, TaskForm, Team, User
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
        teams = []
        for p in user_projects:
            teams.append(p.team_set.all().first())
        print(teams)
        data = {"user": user,
                "teams": teams,
                "projects": page_obj,
                'form': ProjectForm()
                }
        return render(request, 'boards.html', data)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        user = request.user

        if request.POST.get('project_add'):
            form = ProjectForm(request.POST)
            if form.is_valid():
                s_form = form.save(commit=False)
                s_form.owner = user
                s_form.save()

        if request.POST.get('project_update'):
            proj = Project.objects.filter(id=request.POST.get('project_update')).first()
            proj.name = request.POST.get('updateProjectName')
            proj.description = request.POST.get('updateProjectDescription')
            proj.details = request.POST.get('updateProjectDetails')
            proj.save()

        return redirect('boards')


def deleteProject(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    try:
        proj = Project.objects.get(id=id)
    except:
        return redirect('boards')

    if request.user.id == proj.owner.id:
        proj.delete()
    else:
        try:
            team = Team.objects.get(project_id=id)
        except:
            return redirect('boards')

        team.members.remove(request.user)
        team.save()

    return redirect('boards')


def deleteRow(request, id, id_row):
    if not request.user.is_authenticated:
        return redirect('/')

    try:
        row = Row.objects.get(id=id_row)
    except:
        return redirect(f'/boards/{id}')

    if request.user.id == row.project.owner_id:
        row.delete()

    return redirect(f'/boards/{id}')


def deleteMember(request, id, id_member):
    if not request.user.is_authenticated:
        return redirect('/')

    try:
        team = Team.objects.get(project_id=id)
        member = User.objects.get(id=id_member)
    except:
        return redirect('boards')

    if request.user.id == team.project.owner_id:
        team.members.remove(member)
        team.save()

    return redirect('boards')


def deleteTask(request, id, id_task):
    if not request.user.is_authenticated:
        return redirect('/')

    try:
        task = Task.objects.get(id=id_task)
    except:
        return redirect(f'/boards/{id}')

    if request.user.id == task.assigned_to.id or \
            request.user.id == task.project.owner.id:
        task.delete()

    return redirect(f'/boards/{id}')


class Tasks(View):
    def get(self, request, id):

        user = request.user

        if not user.is_authenticated:
            return redirect("/")

        user_projects = Project.objects.filter(team__members__id=user.id)
        proj = Project.objects.filter(id=id).first()

        if proj not in user_projects:
            return redirect('/')

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
                'rows_all': rows,
                "can_add": user == proj.owner,
                "row_form": RowForm(),
                "task_form": TaskForm(),
                }
        return render(request, 'tasks.html', data)

    def post(self, request, id):

        if not request.user.is_authenticated:
            return redirect('/')

        user = request.user
        user_projects = Project.objects.filter(team__members__id=user.id)
        project = Project.objects.filter(id=id).first()

        if project not in user_projects:
            return redirect('/')

        if request.POST.get('row_add'):
            row_form = RowForm(request.POST)
            if row_form.is_valid():
                s_form = row_form.save(commit=False)
                s_form.project = project
                s_form.save()

        if request.POST.get('task_add'):
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                s_form = task_form.save(commit=False)
                s_form.project = project
                s_form.row = Row.objects.filter(id=request.POST.get('row_id')).first()
                s_form.assigned_to = request.user
                s_form.save()

        if request.POST.get('task_update'):
            task = Task.objects.filter(id=request.POST.get('task_update')).first()
            task.name = request.POST.get('updateTaskName')
            task.description = request.POST.get('updateTaskDescription')
            task.end_time = request.POST.get('updateTaskTime')
            task.save()

        if request.POST.get('task_edit_row_right'):
            task = Task.objects.filter(id=request.POST.get('task_id')).first()
            rows = list(project.row_set.all())
            row = Row.objects.filter(id=request.POST.get('task_edit_row_right')).first()
            print(rows)
            print(rows.index(row))
            try:
                task.row = rows[rows.index(row)+1]
            except IndexError:
                task.row = rows[0]
            task.save()
        if request.POST.get('task_edit_row_left'):
            task = Task.objects.filter(id=request.POST.get('task_id')).first()
            rows = list(project.row_set.all())
            row = Row.objects.filter(id=request.POST.get('task_edit_row_left')).first()
            print(rows)
            print(rows.index(row))
            try:
                task.row = rows[rows.index(row)-1]
                task.save()
            except IndexError:
                pass

        return redirect(f'/boards/{id}')


def addMember(request, key):
    if not request.user.is_authenticated:
        return redirect('/')

    user = request.user
    project = Project.objects.filter(key=key).first()

    team = project.team_set.all().first()
    team.members.add(user)
    team.save()

    return redirect('boards')



# class ManegeTasks(View):
#   def post(self, request, id):
#      if not request.user.is_authenticated:
#         response = JsonResponse({"error": "Invalid User"})
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

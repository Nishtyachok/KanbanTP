from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class Projects(View):
    #@login_required
    def get(self, request):
        return render(request, 'boards.html')

    # @login_required
    def post(self, request):
        return redirect('boards')


class Tasks(View):
    # @login_required
    def get(self, request, id):
        return HttpResponse(id)

    # @login_required
    def post(self, request):
        return redirect('tasks', id=id)

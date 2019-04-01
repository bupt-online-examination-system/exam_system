from django.shortcuts import render
from django.http import HttpResponse
from graduation_project import settings
from django.contrib.auth.decorators import login_required

def adminstrator_login(request): #管理员界面模板
    return render(request, "administrator_login.html")

def student_list(request):    #在线考试待考课程列表界面
    return render(request, "student_list.html")

def teacher_list(request):    #在线考试待考课程列表界面
    return render(request, "teacher_list.html")

def question_list(request):    #在线考试待考课程列表界面
    return render(request, "question_list.html")
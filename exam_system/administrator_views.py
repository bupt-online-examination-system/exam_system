from django.shortcuts import render
from django.http import HttpResponse
from graduation_project import settings
from django.contrib.auth.decorators import login_required

def administrator_login(request): #管理员界面模板
    return render(request, "administrator_login.html")

def administrator_mlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_mlist.html")

def administrator_tlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_tlist.html")

def administrator_qlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_qlist.html")

def administrator_tlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_tlist.html")

def administrator_fmanage(request):    #在线考试待考课程列表界面
    return render(request, "administrator_fmanage.html")

def administrator_feedback(request):    #在线考试待考课程列表界面
    return render(request, "administrator_feedback.html")

def administrator_studentlist(request):    #考试成绩界面
    return render(request, "administrator_studentlist.html",locals())

def administrator_teacherlist(request):    #考试成绩界面
    return render(request, "administrator_teacherlist.html",locals())

def administrator_aftlist(request):    #考试成绩界面
    return render(request, "administrator_aftlist.html",locals())

def administrator_uftlist(request):    #考试成绩界面
    return render(request, "administrator_uftlist.html",locals())

from django.shortcuts import render
from django.http import HttpResponse
from graduation_project import settings
from django.contrib.auth.decorators import login_required
import MySQLdb
import re
import random
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse
from django.views.generic.base import View
from.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request): #管理员界面模板
    return render(request, "index.html")

def administrator_login(request):
    return render(request,"administrator_login.html")

def administrator_index_tea(request): #管理员界面模板
    if request.method == "GET":
        return render(request, "administrator_index_tea.html")
    elif request.method == "POST":
        login_user = request.POST.get('userId')
        login_password = request.POST.get("passWord")
        login_user_type = list(Person.objects.filter(userId = login_user).values_list('userType',flat=True))
        user = list(Person.objects.filter(userId=login_user, passWord=login_password).values_list('userId',flat=True))
        request.session["userId"] = login_user
        print(login_user)
        request.session["passWord"] = login_password
        request.session["userType"] = login_user
        request.session["user"] = user
        return render(request, "teacher_homepage.html",locals())

def administrator_index_adm(request): #管理员界面模板
    if request.method == "GET":
        return render(request, "administrator_index_adm.html")
    elif request.method == "POST":
        login_user = request.POST.get('userId')
        login_password = request.POST.get("passWord")
        login_user_type = list(Person.objects.filter(userId = login_user).values_list('userType',flat=True))
        user = list(Person.objects.filter(userId=login_user, passWord=login_password).values_list('userId',flat=True))
        request.session["userId"] = login_user
        request.session["passWord"] = login_password
        request.session["userType"] = login_user
        request.session["user"] = user
        return render(request, "administrator_homepage.html",locals())

def administrator_index_stu(request): #管理员界面模板
    return render(request, "administrator_index_stu.html")

def administrator_homepage(request):    #在个人主页界面
    login_user = request.POST.get('userId')
    login_password = request.POST.get("passWord")
    login_user_type = list(Person.objects.filter(userId=login_user).values_list('userType',flat=True))
    administrator_name = Person.objects.filter(userId=login_user).values('userName')
    count = Person.objects.filter(userId=login_user).count()
    if count == 1 and login_user_type[0] == 1:
        real_password = list(Person.objects.filter(userId=login_user).values_list('passWord',flat=True))
        if login_password == real_password[0]:
            return render(request, "administrator_homepage.html", locals())
        else:
            return render(request, 'administrator_error_adm.html')
    else:
        return render(request, 'administrator_error_adm.html')


def administrator_error_tea(request): #管理员界面模板
    return render(request, "administrator_error_tea.html")

def administrator_error_adm(request):
    return render(request, "administrator_error_adm.html")

def administrator_error_stu(request): #管理员界面模板
    return render(request, "administrator_error_stu.html")

def administrator_mlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_mlist.html")

def administrator_tlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_tlist.html")

def administrator_qlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_qlist.html")

def administrator_fmanage(request):    #在线考试待考课程列表界面
    return render(request, "administrator_fmanage.html")

def administrator_feedback(request):    #在线考试待考课程列表界面
    return render(request, "administrator_feedback.html")

def administrator_studentlist(request):    #考试成绩界面
    return render(request, "administrator_studentlist.html",locals())

def administrator_teacherlist(request):    #考试成绩界面
    return render(request, "administrator_teacherlist.html",locals())

def administrator_aftlist(request):    #已通过成绩页面
    return render(request, "administrator_aftlist.html", locals())

def administrator_uftlist(request):    #未通过成绩界面
    return render(request, "administrator_uftlist.html", locals())



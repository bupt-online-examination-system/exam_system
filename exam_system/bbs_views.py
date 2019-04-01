from django.shortcuts import render
from.models import *
from django.contrib.auth.decorators import login_required
import time

# import pandas
from graduation_project import settings
from django.http import HttpResponse


#@login_required
#python的装饰器，相当于java中的注解     @login_required表示必须登录才能访问，否则跳转到登录页面，在settings.py中配置LGOIN_URL参数（即登陆url）
def event_manage(request):
    course_info=Course.objects.all() #全部用 all，部分条件用filter
    return render(request, "guest_manage.html", locals())

def course_forum(request):
    courseId = request.GET.get("courseId")
    course_forum_info = Forum.objects.filter(courseId=courseId)
    return render(request, "course_forum.html", locals())

def course_post(request):
    return render(request, "course_post.html")

def new_post(request):
    if request.method == "GET":
        return render(request, "new_post.html")
    elif request.method == "POST":
        subject = request.POST.get('subject','')
        message = request.POST.get('message','')
        new_post=Forum.objects.create(content=message,title=subject,courseId=1,answerId_id=12,questionId_id=123)

        return render(request, "course_forum.html")

def edit_post(request):
    if request.method == "GET":
        return render(request, "edit_post.html")
    elif request.method == "POST":
        subject = request.POST.get('subject','无标题')
        message = request.POST.get('message','无内容')

        return render(request, "course_forum.html")

def answer_post(request):
    return render(request, "answer_post.html")
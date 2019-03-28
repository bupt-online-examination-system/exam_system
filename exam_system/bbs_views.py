from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

# import pandas
from graduation_project import settings
from django.http import HttpResponse


#@login_required
#python的装饰器，相当于java中的注解     @login_required表示必须登录才能访问，否则跳转到登录页面，在settings.py中配置LGOIN_URL参数（即登陆url）
def event_manage(request):
    return render(request, "guest_manage.html")

def course_forum(request):
    return render(request, "course_forum.html")

def course_post(request):
    return render(request, "course_post.html")
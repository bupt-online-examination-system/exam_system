from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

# import pandas
from graduation_project import settings
from django.http import HttpResponse


#@login_required
#python的装饰器，相当于java中的注解     @login_required表示必须登录才能访问，否则跳转到登录页面，在settings.py中配置LGOIN_URL参数（即登陆url）
def event_manage(request):
    if request.method == 'GET':
        exam_time =  10     #获取设置的考试时间，转成秒
        now_time = time.time()
        #当前时间戳    这里应该判断一下该学生的状态是考试中还是未考试，如果是考试中，从数据库获取end_time(之后会把考试答卷改成异步上传，每次改动都传)。如果是未考试才获取当前时间
        end_time = now_time + exam_time#截止时间戳
        return render(request, "guest_manage.html", {"end_time":end_time*1000})#js中的时间戳是毫秒，转换一下
    elif request.method == 'POST':
        #存到数据库     算分，显示在页面上
        pass
        return render(request, "guest_manage.html")

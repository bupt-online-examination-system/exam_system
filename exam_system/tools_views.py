from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time
import random
# import pandas
from graduation_project import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from xlwt import *
#@login_required
#python的装饰器，相当于java中的注解     @login_required表示必须登录才能访问，否则跳转到登录页面，在settings.py中配置LGOIN_URL参数（即登陆url）
def start_exam(request):
    if request.method == 'GET':
        exam_time =  10     #获取设置的考试时间，转成秒
        now_time = time.time()
        #当前时间戳    这里应该判断一下该学生的状态是考试中还是未考试，如果是考试中，从数据库获取end_time(之后会把考试答卷改成异步上传，每次改动都传)。如果是未考试才获取当前时间
        end_time = now_time + exam_time#截止时间戳
        return render(request, "exam_interface.html",{"end_time":end_time*1000})#js中的时间戳是毫秒，转换一下
    elif request.method == 'POST':
        #存到数据库     算分，显示在页面上
        pass
        return render(request, "exam_result.html")

def get_psw(request):
    #为了防止代考，给每个考生生成6位随机口令 与考号绑定
    if request.method == 'GET':
        return render(request, "psw_out.html")
    elif request.method == "post":
        path = request['path']#或者request.POST.get('path'):
        chars = 'abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # 随机产生6个不同字符
        random_chars = "".join(random.sample(chars, 6))


        return render(request, "psw_out.html")






def send_email(request):
    if request.method == "GET":
        return render(request, "send_mail.html")
    elif request.method == "POST":
        name = request.POST.get('name', '')
        subject = request.POST.get('subject','无标题')
        text_content = request.POST.get('message','无内容')#提交的时候前端验证一下，不允许发空邮件   未完成
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = ['245213994@qq.com']  # 可以是多个
        send_mail(
            subject=subject,
            message=text_content,
            from_email=from_email,
            recipient_list=to_email
        )
        return HttpResponse('发送成功')#然后返回主页  未完成


def data_in(request):
    if request.method == "GET":
        return render(request, "data_in.html")
    elif request.method == "POST":
        data_file = request.POST.get('txt',None)
        print(type(data_file))
        print(data_file)
        return HttpResponse('发送成功')  # 然后返回主页

def data_out(request):
    pass
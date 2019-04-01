from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time
import random
# import pandas
from graduation_project import settings
from django.http import HttpResponse
from django.core.mail import send_mail
import xlrd
from .models import *



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

        from django.apps import apps
        tables = list(apps.get_app_config('exam_system').get_models())
        return render(request, "data_in.html",locals())



    elif request.method == "POST":

        from django.apps import apps
        app_models = list(apps.get_app_config('exam_system').get_models())

        # print(type(Person))
        # print(app_models[0])


        f = request.FILES.get('file')
        table_num = request.POST.get('table')

        model_class = app_models[int(table_num)]
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数



            for i in range(1, rows):
                rowVlaues = table.row_values(i)
                rowVlaues = tuple(rowVlaues)
                if table_num == '0':
                    Person.objects.create(userId=str(int(rowVlaues[0])),
                                          userType=int(rowVlaues[1]),
                                          userName=rowVlaues[2],
                                          passWord = rowVlaues[3])
                # elif table_num == '1':
                #     Course.objects.create(
                #     courseId = str(int(rowVlaues[0])),
                #     teacherId = str(),
                #                                   on_delete=models.CASCADE)  # 教师id
                #     studentId = models.ForeignKey('Person', related_name='student_course',
                #                                   on_delete=models.CASCADE)  # 学生id
                #     courseName = models.CharField(max_length=50)  # 课程名称
                #     isOver
                #     )
                #     elif table_num == '2':
                #     elif table_num == '3':
                #     elif table_num == '4':
                #     elif table_num == '5':
                #     elif table_num == '6':
                #     elif table_num == '7':
                #     elif table_num == '8':





    return HttpResponse('导入成功')



def data_out(request):
    pass


# def ajax_post(request):
#     for i in range():
#     a = request.GET.get("a")
#     b = request.GET.get("b")
#     n = int(a) * int(b)
#     return HttpResponse(str(n))
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
from datetime import datetime


#@login_required
#python的装饰器，相当于java中的注解     @login_required表示必须登录才能访问，否则跳转到登录页面，在settings.py中配置LGOIN_URL参数（即登陆url）
def exam_details(request):

    if request.method == 'GET':#获取本次考试的所有数据
        exam_time = 60    #获取设置的考试时间，转成秒         写死成1小时
        # now_time = time.time()
        # end_time = now_time + exam_time#截止时间戳
        # end_time = 1000*end_time

        studentId = request.session.get('studentId')
        studentName = Person.objects.filter(userId=studentId).values('userName')
        courseId = request.GET.get("courseId")
        #examId = list(Exam.objects.filter(studentId=studentId,courseId=courseId,isOver=1).values_list('examId',flat=True).order_by('examId')) #得到该学生该课程下一次考试的examId
        #exam = Exam.objects.filter(studentId=studentId, courseId=courseId)[0]
        exam = Exam.objects.filter(studentId=studentId,courseId=courseId,isOver=1).order_by('examId')[0] #得到该学生该课程下一次考试的examId
        print(exam)
        course = Course.objects.filter(courseId = courseId)
        choice_question_info = []
        fill_question_info = []



        if exam.isOver == 1:#考试未结束
            # print(exam.start_time)
            # print(type(exam.start_time.strftime('%Y-%m-%d %H:%M:%S')))
            if exam.start_time.strftime('%Y-%m-%d %H:%M:%S') == '1970-01-01 00:00:00':#考试未开始
                print("开始考试")
                exam.start_time = datetime.now()
                exam.save()

                end_time = (exam_time + time.mktime(exam.start_time.timetuple()))*1000
                print(end_time)
            else:
                end_time = (exam_time + time.mktime(datetime.now().timetuple())) * 1000
                print(end_time)
            exam_question_info = ExamQuestion.objects.filter(examId=exam.examId).values('questionId', 'type','answer')
            for i in exam_question_info:
                if i['type'] == 1:
                    choice_question_info.append(
                        [ChoiceQuestion.objects.filter(type=1,choiceId=i['questionId'])[0]  , i['answer']]
                    )
                elif i['type'] == 2:
                    fill_question_info.append(
                        [FillInTheBlank.objects.filter(type=1,fillId=i['questionId'])[0],i['answer']]
                    )

            return render(request,"exam_interface.html",locals())#js中的时间戳是毫秒，转换一下

        elif exam.isOver == 2:  # 考试中途退出再打开
            return HttpResponse('考试已结束')



    elif request.method == 'POST':

        exam_id = int(request.POST.get("exam"))
        studentId = request.session.get('studentId')
        studentName = Person.objects.filter(userId=studentId).values('userName')[0]['userName']

        exam = Exam.objects.filter(examId = exam_id)[0]
        print(studentName)
        exam_question_info = ExamQuestion.objects.filter(examId=exam.examId).values('questionId', 'type', 'answer')
        right_choice = 0
        right_fill  = 0
        for i in exam_question_info:
            if i['type'] == 1:
                if ChoiceQuestion.objects.filter(type=1, choiceId=i['questionId'])[0].answer == i['answer']:
                    i.isRight = 1
                    right_choice+=1
                else:
                    i.isRight = 0
            elif i['type'] == 2:
                if FillInTheBlank.objects.filter(type=1, fillId=i['questionId'])[0].answer == i['answer']:
                    i.isRight = 1
                    right_choice+=1
                else:
                    i.isRight = 0
        score = (right_choice+right_fill)*5
        exam.score =  score  #写死  每题5分
        exam.isOver = 2
        exam.save()

        print(exam.examId)
        print(score)
        return render(request, "exam_result.html",locals())

def reset_psw(request):
    #为了防止代考，给所有考生重置密码
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


def ajax_post(request):
    stu = request.session.get('studentId')
    exam = int(request.POST.get("exam"))
    type_ = int(request.POST.get("type"))
    num = request.POST.get("id")
    answer = request.POST.get("answer")
    print(stu,exam,type_,num,answer)


    instance = ExamQuestion.objects.filter(examId = exam,type = type_,questionId = num)
    if instance:
        instance[0].answer = answer
        instance[0].save()
    else:
        ExamQuestion.objects.create(examId = exam,type = type_,answer = answer,questionId = num)
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
from xlwt import Workbook
from django.contrib import messages


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
        exam_list = Exam.objects.filter(studentId=studentId,courseId=courseId,isOver=1).order_by('examId')
        if exam_list:
            exam = exam_list[0]
        else:
            return HttpResponse('现在不能考试')
        print(exam)
        course = Course.objects.filter(courseId = courseId)
        choice_question_info = []
        fill_question_info = []



        if exam.isOver == 1:#考试未结束
            user = request.user
            user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')

            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            History.objects.create(
                studentId = Person.objects.get(userId=studentId),
                courseId = Course.objects.get(courseId=courseId),
                examId = exam,
                ip = ip,
                time = datetime.now(),
            )
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

        elif exam.isOver == 2:
            messages.success(request, "考试已结束")
            return render(request, "personal_homepage.html", locals())



    elif request.method == 'POST':
        print("交卷")
        exam_id = int(request.POST.get("exam"))
        print("试卷id"+str(exam_id))
        studentId = request.session.get('studentId')
        studentName = Person.objects.filter(userId=studentId).values('userName')[0]['userName']

        exam = Exam.objects.filter(examId = exam_id)[0]
        print(studentName)
        exam_question_info = ExamQuestion.objects.filter(examId=exam.examId)
        right_choice = 0
        right_fill  = 0
        for i in exam_question_info:
            if i.type == 1:
                if ChoiceQuestion.objects.filter(type=1, choiceId=i.questionId)[0].answer == i.answer:
                    i.isRight = 1
                    right_choice+=1
                else:
                    i.isRight = 0
            elif i.type == 2:
                if FillInTheBlank.objects.filter(type=1, fillId=i.questionId)[0].answer == i.answer:
                    i.isRight = 1
                    right_choice+=1
                else:
                    i.isRight = 0
            i.save()
        score = (right_choice+right_fill)*5
        exam.score =  score  #写死  每题5分
        exam.isOver = 2
        exam.save()

        print(exam.examId)
        print(score)
        return render(request, "exam_result.html",locals())

def reset_psw(request):
    #为了防止代考，给所有考生重置密码
    person_list = Person.objects.all()
    if request.method == 'GET':

        # path = request['path']#或者request.POST.get('path'):
        chars = 'abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # 随机产生6个不同字符
        for i in person_list:
            i.passWord = "".join(random.sample(chars, 6))
            i.save()


        person_list = Person.objects.all()
        if person_list:
            # 创建工作薄
            ws = Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, "考生姓名")
            w.write(0, 1, "密码")


            excel_row = 1
            for obj in person_list:
                w.write(excel_row, 0, obj.userName)
                w.write(excel_row, 1, obj.passWord)

                excel_row += 1

            ws.save(r"file\考试名单.xls")
            # return HttpResponse('导出成功')
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
        try:
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

                if table_num == '0':

                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)
                        if type(rowVlaues[3])==float and int(rowVlaues[3])==rowVlaues[3]:
                            passWord = str(int(rowVlaues[3]))
                        else:
                            passWord = rowVlaues[3]
                        Person.objects.create(
                              userId=int(rowVlaues[0]),
                              userType=int(rowVlaues[1]),
                              userName=str(rowVlaues[2]),
                              passWord=passWord,
                              )

                elif table_num == '1':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)
                        Course.objects.create(
                            courseId = int(rowVlaues[0]),
                            teacherId = Person.objects.get(userId = int(rowVlaues[1])),
                            courseName=str(rowVlaues[2]),
                            isOver = int(rowVlaues[3])
                        )


                elif table_num == '2':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        CourseStudent.objects.create(
                            courseId=Course.objects.get(courseId = int(rowVlaues[0])),
                            studentId=Person.objects.get(userId = int(rowVlaues[1])),
                        )
                elif table_num == '3':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        if rowVlaues[7]:
                            start_time = xlrd.xldate.xldate_as_datetime(rowVlaues[7], 0)
                            Exam.objects.create(
                                examId=int(rowVlaues[0]),
                                courseId = Course.objects.get(courseId = rowVlaues[1]),
                                studentId = Person.objects.get(userId = rowVlaues[2]),
                                isOver = int(rowVlaues[3]),
                                score = int(rowVlaues[4]),
                                type = int(rowVlaues[5]),
                                weight = int(rowVlaues[6]),
                                start_time = start_time,
                            )
                        else:
                            Exam.objects.create(
                                examId=int(rowVlaues[0]),
                                courseId=Course.objects.get(courseId=rowVlaues[1]),
                                studentId=Person.objects.get(userId=rowVlaues[2]),
                                isOver=int(rowVlaues[3]),
                                score=int(rowVlaues[4]),
                                type=int(rowVlaues[5]),
                                weight=int(rowVlaues[6]),
                            )
                elif table_num == '4':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        if type(rowVlaues[2])==float and int(rowVlaues[2])==rowVlaues[2]:
                            answer = str(int(rowVlaues[2]))
                        else:
                            answer = rowVlaues[2]
                        ExamQuestion.objects.create(
                            examId = Exam.objects.get(int(examId = rowVlaues[0])),
                            questionId = int(rowVlaues[1]),
                            answer = answer,
                            isRight = int(rowVlaues[3]),
                            type = int(rowVlaues[4]),
                        )

                elif table_num == '5':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        ChoiceQuestion.objects.create(
                            choiceId= int(rowVlaues[0]),
                            courseId =  Course.objects.get(courseId = int(rowVlaues[1])),
                            content =  str(rowVlaues[2]),
                            questionA = str(rowVlaues[3]),
                            questionB =  str(rowVlaues[4]),
                            questionC =  str(rowVlaues[5]),
                            questionD = str(rowVlaues[6]),
                            answer = str(rowVlaues[7]),
                            type = int(rowVlaues[8]),
                        )
                elif table_num == '6':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        FillInTheBlank.objects.create(
                            fillId = int(rowVlaues[0]),
                            courseId = Course.objects.get(courseId = int(rowVlaues[1])),
                            content = str(rowVlaues[2]),
                            answer = str(rowVlaues[3]),
                            type = int(rowVlaues[4]),
                        )
                elif table_num == '7':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        Grade.objects.create(
                            studentId = Person.objects.get(userId=int(rowVlaues[0])),
                            courseId = Course.objects.get(courseId = int(rowVlaues[1])),
                            grade=int(rowVlaues[2]),
                            isPass=int(rowVlaues[3]),
                        )

                elif table_num == '8':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        MistakesCollection.objects.create(
                            studentId=Person.objects.get(userId=int(rowVlaues[0])),
                            courseId=Course.objects.get(courseId=int(rowVlaues[1])),
                            questionId=int(rowVlaues[2]),
                            type=int(rowVlaues[3]),
                        )

                elif table_num == '9':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        ForumQuestion.objects.create(
                            postId =  int(rowVlaues[0]),
                            questionId = Person.objects.get(questionId = int(rowVlaues[1])),
                            content = rowVlaues[2],
                            title = rowVlaues[3],
                            courseId = Course.objects.get(courseId = rowVlaues[4]),
                            postTime = rowVlaues[5],
                            topTime = rowVlaues[6],
                            answerNum = int(rowVlaues[7]),
                        )
                elif table_num == '10':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        ForumAnswer.objects.create(
                            postId = int(rowVlaues[0]),
                            answerId = int(rowVlaues[1]),
                            content = rowVlaues[2],
                            answerTime = rowVlaues[3],
                        )

                elif table_num == '11':
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues = tuple(rowVlaues)

                        History.objects.create(
                            studentId=Person.objects.get(userId=int(rowVlaues[0])),
                            courseId=Course.objects.get(courseId=int(rowVlaues[1])),
                            examId = Exam.objects.get(examId = int(rowVlaues[2])),
                            ip = rowVlaues[3],
                            time = rowVlaues[4],
                        )






        except Exception:
            messages.success(request, '导入失败，请检查：1.数据格式是否正确  2.表格中数与数据库中数据主键重复  3.表格与数据库表是否对应  4.是否选择了导入的表格和数据库表')
            return render(request, "data_in.html", locals())

        else:
            messages.success(request, "导入成功")
            return render(request, "data_in.html", locals())



def data_out(request):
    if request.method == "GET":
        from django.apps import apps
        tables = list(apps.get_app_config('exam_system').get_models())
        return render(request, "data_out.html",locals())

    elif request.method == "POST":


        if not request.POST['path'] or not request.POST['table']:
            messages.success(request, '导出失败，输入的路径不正确或未选择数据库表')
            return render(request, "data_out.html", locals())
        path = request.POST['path']
        table_num = request.POST.get('table')



        if table_num == '0':
            person_list = Person.objects.all()
            if person_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "userId")
                w.write(0, 1, "userType")
                w.write(0, 2, "userName")
                w.write(0, 3, "passWord")

                # 写入数据
                excel_row = 1
                for obj in person_list:
                    w.write(excel_row, 0, obj.userId)
                    w.write(excel_row, 1, obj.userType)
                    w.write(excel_row, 2, obj.userName)
                    w.write(excel_row, 3, obj.passWord)

                    excel_row += 1

                ws.save(path + r"\Person.xls")
                messages.success(request, "导入成功")
                return render(request, "data_out.html", locals())



        elif table_num == '1':
            course_list = Course.objects.all()
            if course_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "courseId")
                w.write(0, 1, "teacherId")
                w.write(0, 2, "courseName")
                w.write(0, 3, "isOver")

                # 写入数据
                excel_row = 1
                for obj in course_list:
                    w.write(excel_row, 0, obj.courseId)
                    w.write(excel_row, 1, obj.teacherId)
                    w.write(excel_row, 2, obj.courseName)
                    w.write(excel_row, 3, obj.isOver)

                    excel_row += 1

                ws.save(path + r"\Course.xls")
                messages.success(request, "导入成功")
                return render(request, "data_out.html", locals())



        elif table_num == '2':
            coursestudent_list = CourseStudent.objects.all()
            if coursestudent_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "courseId")
                w.write(0, 1, "studentId")


                # 写入数据
                excel_row = 1
                for obj in coursestudent_list:
                    w.write(excel_row, 0, obj.courseId)
                    w.write(excel_row, 1, obj.teacherId)
                    w.write(excel_row, 2, obj.courseName)
                    w.write(excel_row, 3, obj.isOver)

                    excel_row += 1

                ws.save(path + r"\CourseStudent.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())



        elif table_num == '3':
            exam_list = Exam.objects.all()
            if exam_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "examId")
                w.write(0, 1, "courseId")
                w.write(0, 2, "studentId")
                w.write(0, 3, "isOver")
                w.write(0, 4, "score")
                w.write(0, 5, "type")
                w.write(0, 6, "weight")
                w.write(0, 7, "start_time")


                # 写入数据
                excel_row = 1
                for obj in exam_list:
                    w.write(excel_row, 0, obj.examId)
                    w.write(excel_row, 1, obj.courseId)
                    w.write(excel_row, 2, obj.studentId)
                    w.write(excel_row, 3, obj.isOver)
                    w.write(excel_row, 4, obj.score)
                    w.write(excel_row, 5, obj.type)
                    w.write(excel_row, 6, obj.weight)
                    w.write(excel_row, 7, obj.start_time)

                    excel_row += 1

                ws.save(path + r"\Exam.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())


        elif table_num == '4':
            examquestion_list = ExamQuestion.objects.all()
            if examquestion_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "examId")
                w.write(0, 1, "questionId")
                w.write(0, 2, "answer")
                w.write(0, 3, "isRight")
                w.write(0, 4, "type")
                w.write(0, 5, "checkTime")



                # 写入数据
                excel_row = 1
                for obj in examquestion_list:
                    w.write(excel_row, 0, obj.examId)
                    w.write(excel_row, 1, obj.questionId)
                    w.write(excel_row, 2, obj.answer)
                    w.write(excel_row, 3, obj.isRight)
                    w.write(excel_row, 4, obj.type)
                    w.write(excel_row, 5, obj.checkTime)

                    excel_row += 1

                ws.save(path + r"\Exam.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())


        elif table_num == '5':
            all_list = ChoiceQuestion.objects.all()
            if all_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "choiceId")
                w.write(0, 1, "courseId")
                w.write(0, 2, "content")
                w.write(0, 3, "questionA")
                w.write(0, 4, "questionB")
                w.write(0, 5, "questionC")
                w.write(0, 6, "questionD")
                w.write(0, 7, "answer")
                w.write(0, 8, "type")
                # 写入数据
                excel_row = 1
                for obj in all_list:
                    w.write(excel_row, 0, obj.choiceId)
                    w.write(excel_row, 1, obj.courseId)
                    w.write(excel_row, 2, obj.content)
                    w.write(excel_row, 3, obj.questionA)
                    w.write(excel_row, 4, obj.questionB)
                    w.write(excel_row, 5, obj.questionC)
                    w.write(excel_row, 6, obj.questionD)
                    w.write(excel_row, 7, obj.answer)
                    w.write(excel_row, 8, obj.type)


                    excel_row += 1

                ws.save(path + r"\ChoiceQuestion.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())


        elif table_num == '6':
            all_list = FillInTheBlank.objects.all()
            if all_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "fillId")
                w.write(0, 1, "courseId")
                w.write(0, 2, "content")
                w.write(0, 3, "answer")
                w.write(0, 4, "type")
                # 写入数据
                excel_row = 1
                for obj in all_list:
                    w.write(excel_row, 0, obj.fillId)
                    w.write(excel_row, 1, obj.courseId)
                    w.write(excel_row, 2, obj.content)
                    w.write(excel_row, 3, obj.answer)
                    w.write(excel_row, 4, obj.type)

                    excel_row += 1

                ws.save(path + r"\Exam.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())


        elif table_num == '7':
            all_list = Grade.objects.all()
            if all_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "studentId")
                w.write(0, 1, "courseId")
                w.write(0, 2, "grade")
                w.write(0, 3, "isPass")
                # 写入数据
                excel_row = 1
                for obj in all_list:
                    w.write(excel_row, 0, obj.studentId)
                    w.write(excel_row, 1, obj.courseId)
                    w.write(excel_row, 2, obj.grade)
                    w.write(excel_row, 3, obj.isPass)

                    excel_row += 1

                ws.save(path + r"\Grade.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())


        elif table_num == '8':
            all_list = MistakesCollection.objects.all()
            if all_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "studentId")
                w.write(0, 1, "courseId")
                w.write(0, 2, "questionId")
                w.write(0, 3, "type")
                # 写入数据
                excel_row = 1
                for obj in all_list:
                    w.write(excel_row, 0, obj.studentId)
                    w.write(excel_row, 1, obj.courseId)
                    w.write(excel_row, 2, obj.questionId)
                    w.write(excel_row, 3, obj.type)

                    excel_row += 1

                ws.save(path + r"\MistakesCollection.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())

        elif table_num == '9':
            all_list = ForumQuestion.objects.all()
            if all_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "postId")
                w.write(0, 1, "questionId")
                w.write(0, 2, "content")
                w.write(0, 3, "title")
                w.write(0, 4, "courseId")
                w.write(0, 5, "postTime")
                w.write(0, 6, "topTime")
                w.write(0, 7, "answerNum")
                # 写入数据
                excel_row = 1
                for obj in all_list:
                    w.write(excel_row, 0, obj.postId)
                    w.write(excel_row, 1, obj.questionId)
                    w.write(excel_row, 2, obj.content)
                    w.write(excel_row, 3, obj.title)
                    w.write(excel_row, 4, obj.courseId)
                    w.write(excel_row, 5, obj.postTime)
                    w.write(excel_row, 6, obj.topTime)
                    w.write(excel_row, 7, obj.answerNum)

                    excel_row += 1

                ws.save(path + r"\ChoiceQuestion.xls")
                messages.success(request, "导出成功")
                return render(request, "ForumQuestion.html", locals())


        elif table_num == '10':
            all_list = ForumAnswer.objects.all()
            if all_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "postId")
                w.write(0, 1, "answerId")
                w.write(0, 2, "courseId")
                w.write(0, 3, "content")
                w.write(0, 4, "answerTime")
                # 写入数据
                excel_row = 1
                for obj in all_list:
                    w.write(excel_row, 0, obj.postId)
                    w.write(excel_row, 1, obj.answerId)
                    w.write(excel_row, 2, obj.courseId)
                    w.write(excel_row, 3, obj.content)
                    w.write(excel_row, 4, obj.answerTime)

                    excel_row += 1

                ws.save(path + r"\ForumAnswer.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())

        elif table_num == '11':
            all_list = History.objects.all()
            if all_list:
                # 创建工作薄
                ws = Workbook(encoding='utf-8')
                w = ws.add_sheet(u"数据报表第一页")
                w.write(0, 0, "studentId")
                w.write(0, 1, "courseId")
                w.write(0, 2, "examId")
                w.write(0, 3, "ip")
                w.write(0, 4, "time")
                # 写入数据
                excel_row = 1
                for obj in all_list:
                    w.write(excel_row, 0, obj.studentId)
                    w.write(excel_row, 1, obj.courseId)
                    w.write(excel_row, 2, obj.examId)
                    w.write(excel_row, 3, obj.ip)
                    w.write(excel_row, 4, obj.time)

                    excel_row += 1

                ws.save(path + r"\History.xls")
                messages.success(request, "导出成功")
                return render(request, "data_out.html", locals())
def ajax_post(request):
    print("保存试卷改动")
    stu = request.session.get('studentId')
    exam = int(request.POST.get("exam"))
    type_ = int(request.POST.get("type"))
    num = request.POST.get("id")
    answer = request.POST.get("answer")
    time = request.POST.get("time")
    print(stu,exam,type_,num,answer,time)


    instance = ExamQuestion.objects.filter(examId = exam,type = type_,questionId = num)
    if instance:

        instance[0].checkTime += int(time)
        instance[0].answer = answer
        instance[0].save()
    else:
        ExamQuestion.objects.create(examId = exam,type = type_,answer = answer,questionId = num,checkTime=time)
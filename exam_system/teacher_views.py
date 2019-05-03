from django.shortcuts import render
from.models import *
from django.contrib.auth.decorators import login_required
from graduation_project import settings
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.aggregates import Min

def teacher_login(request): #教师界面模板
    return render(request, "teacher_login.html")

def course_name(request):    #所授课程界面
    teacherId = request.session.get('teacherId')
    teacherName = Person.objects.filter(userId=teacherId).values('userName')
    teacher_info = Course.objects.filter(teacherId=teacherId).values('courseId')
    course_info = Course.objects.all().values('courseId', 'courseName')
    return render(request, "course_name.html", locals())

def first_exam(request):    #第一次月考
    teacherId = request.session.get('teacherId')
    teacherName = Person.objects.filter(userId=teacherId).values('userName')
    courseId = request.GET.get('courseId')
    exam_info = Exam.objects.filter(courseId=courseId,type=1).values('score','studentId','examId')
    student_info = Person.objects.all().values('userId', 'userName')
    return render(request, "first_exam.html", locals())

def second_exam(request):    #第二次月考
    teacherId = request.session.get('teacherId')
    teacherName = Person.objects.filter(userId=teacherId).values('userName')
    courseId = request.GET.get('courseId')
    exam_info = Exam.objects.filter(courseId=courseId, type=2).values('score', 'studentId')
    student_info = Person.objects.all().values('userId', 'userName')
    return render(request, "second_exam.html", locals())

def third_exam(request):    #第三次月考
    teacherId = request.session.get('teacherId')
    teacherName = Person.objects.filter(userId=teacherId).values('userName')
    courseId = request.GET.get('courseId')
    exam_info = Exam.objects.filter(courseId=courseId, type=3).values('score', 'studentId')
    student_info = Person.objects.all().values('userId', 'userName')
    return render(request, "third_exam.html", locals())

def final_exam(request):    #最后一次考试
    teacherId = request.session.get('teacherId')
    teacherName = Person.objects.filter(userId=teacherId).values('userName')
    courseId = request.GET.get('courseId')
    exam_info = Exam.objects.filter(courseId=courseId, type=4).values('score', 'studentId')
    student_info = Person.objects.all().values('userId', 'userName')
    return render(request, "final_exam.html", locals())

def exam_number(request):    #选择第几次考试
    teacherId = request.session.get('teacherId')
    teacherName = Person.objects.filter(userId=teacherId).values('userName')
    courseId = request.GET.get('courseId')
    courseName= Course.objects.filter(courseId=courseId).values('courseName')
    return render(request, "exam_number.html",locals())

def student_name(request):    #学生名单界面
    return render(request, "student_name.html")

def exam_specification(request):    #选择试卷类型界面
    return render(request, "exam_specification.html")

def teacher_homepage(request):    #教师主页界面
    # if request.method == "GET":
    #     request.session.get('teacherId')
    #     teacherName = Person.objects.filter(userId=teacherId).values('userName')
        return render(request, "teacher_homepage.html", locals())
    # elif request.method == "POST":
    #     request.post.get = 2
    #     teacherId = request.session.get('teacherId')
    #     teacherName = Person.objects.filter(userId=teacherId).values('userName')
    #     return render(request, "administrator_error_tea.html",locals())


def student_detail(request):    #学生具体信息界面
    teacherId = request.session.get('teacherId')
    teacherName = Person.objects.filter(userId=teacherId).values('userName')
    examId = request.GET.get(examId)
    exam_info = ExamQuestion.objects.filter(examId=examId).values('questionId','isRight')
    return render(request, "student_detail.html", locals())


def all_student(request):    #全部学生成绩分析界面
    examId=request.GET.get(examId)
    return render(request, "all_student.html",locals())

def question_added(request):    #试题添加界面
    return render(request, "question_added.html")

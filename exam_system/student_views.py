from django.shortcuts import render
from.models import *
from django.contrib.auth.decorators import login_required
from graduation_project import settings
from django.http import HttpResponse
studentId = 1
def student_login(request): #学生界面模板
    return render(request, "student_login.html")

def exam_list(request):    #在线考试待考课程列表界面
    return render(request, "exam_list.html")

def practice_list(request):    #练习课程列表界面
    return render(request, "practice_list.html")

def personal_homepage(request):    #在个人主页界面
    return render(request, "personal_homepage.html")

def score_query(request):    #考试成绩界面
    return render(request, "score_query.html")

def pass_score_query(request):    #全部及格成绩
    pass_score_info = Grade.objects.filter(studentId=studentId, grade__gte=60).values('courseId','grade')
    course_info = Course.objects.all().values('courseId','courseName').distinct()
    return render(request, "pass_score_query.html", locals())

def fail_score_query(request):    #不及格成绩
    fail_score_info = Grade.objects.filter(studentId=studentId, grade__gte=0,grade__lt=60).values('courseId','grade')
    course_info = Course.objects.all().values('courseId','courseName').distinct()
    return render(request, "fail_score_query.html", locals())

def exam_details(request):    #课程考试信息详情界面
    return render(request, "exam_details.html")
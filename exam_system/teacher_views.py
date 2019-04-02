from django.shortcuts import render
from django.http import HttpResponse
from graduation_project import settings
from django.contrib.auth.decorators import login_required

def teacher_login(request): #教师界面模板
    return render(request, "teacher_login.html")

def student_name(request):    #学生名单界面
    return render(request, "student_name.html")

def exam_specification(request):    #选择试卷类型界面
    return render(request, "exam_specification.html")

def teacher_homepage(request):    #教师主页界面
    return render(request, "teacher_homepage.html")

def student_detail(request):    #学生具体信息界面
    return render(request, "student_detail.html")

def all_student(request):    #全部学生成绩分析界面
    return render(request, "all_student.html")

def question_added(request):    #试题添加界面
    return render(request, "question_added.html")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from graduation_project import settings
from django.http import HttpResponse
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

def exam_details(request):    #课程考试信息详情界面
    return render(request, "exam_details.html")
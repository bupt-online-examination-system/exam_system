from django.shortcuts import render
from.models import *
from django.contrib.auth.decorators import login_required
from graduation_project import settings
from django.http import HttpResponse
def student_login(request): #学生界面模板
    return render(request, "student_login.html",locals())

def exam_list(request):    #在线考试待考课程列表界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    return render(request, "exam_list.html",locals())

def practice_list(request):    #练习课程列表界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    return render(request, "practice_list.html",locals())

def personal_homepage(request):    #在个人主页界面
    request.session['studentId'] = 1
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    return render(request, "personal_homepage.html",locals())

def score_query(request):    #考试成绩界面
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    return render(request, "score_query.html",locals())

def pass_score_query(request):    #全部及格成绩
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    pass_score_info = Grade.objects.filter(studentId=studentId, isPass=1).values('courseId','grade')
    course_info = Course.objects.all().values('courseId','courseName')
    return render(request, "pass_score_query.html", locals())

def fail_score_query(request):    #不及格成绩
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    fail_score_info = Grade.objects.filter(studentId=studentId, isPass=2).values('courseId','grade')
    course_info = Course.objects.all().values('courseId','courseName')
    return render(request, "fail_score_query.html", locals())

def pass_exam_details(request):    #已通过课程考试信息详情界面
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")
    exam_details_info = Exam.objects.filter(courseId=courseId).values('type','score')
    return render(request, "pass_exam_details.html", locals())

def fail_exam_details(request):    #未通过课程考试信息详情界面
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")
    exam_details_info = Exam.objects.filter(courseId=courseId).values('type','score')
    return render(request, "fail_exam_details.html", locals())

def exam_schedule(request):    #待考课程界面
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    exam_schedule_info = Course.objects.filter(isOver=1).values('courseId','courseName') #找出期末考未结束的课
    return render(request, "exam_schedule.html", locals())

def exam_schedule_details(request):    #待考课程考试信息详情界面
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")
    exam_details_info = Exam.objects.filter(courseId=courseId).values('type','score')
    return render(request, "exam_schedule_details.html", locals())

def post_record(request):    #发帖记录
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    forum_question_info = ForumQuestion.objects.filter(questionId=studentId).values('title','courseId','postId')
    course_info = Course.objects.all().values('courseId','courseName')
    return render(request, "post_record.html", locals())
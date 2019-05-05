from django.shortcuts import render
from django.http import HttpResponse
from graduation_project import settings
from django.contrib.auth.decorators import login_required
import MySQLdb
import re
import random
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse
from django.views.generic.base import View
from.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request): #管理员界面模板
    return render(request, "index.html")

def administrator_login(request):
    return render(request,"administrator_login.html")

def administrator_index_tea(request): #管理员界面模板
    return render(request, "administrator_index_tea.html")

def administrator_index_adm(request): #管理员界面模板
    return render(request, "administrator_index_adm.html")

def administrator_index_stu(request): #管理员界面模板
    return render(request, "administrator_index_stu.html")

def administrator_error_tea(request): #管理员界面模板
    return render(request, "administrator_error_tea.html")

def administrator_error_adm(request):
    return render(request, "administrator_error_adm.html")

def administrator_error_stu(request): #管理员界面模板
    return render(request, "administrator_error_stu.html")

def administrator_member_list(request):    #在线考试待考课程列表界面
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
        return render(request, "administrator_member_list.html", locals())
    elif request.method == "POST":
        login_user = request.POST.get('userId')
        login_password = request.POST.get("passWord")
        login_user_type = list(Person.objects.filter(userId=login_user).values_list('userType', flat=True))
        administrator_name = Person.objects.filter(userId=login_user).values('userName')
        count = Person.objects.filter(userId=login_user).count()
        if count == 1 and login_user_type[0] == 1:
            real_password = list(Person.objects.filter(userId=login_user).values_list('passWord', flat=True))
            if login_password == real_password[0]:
                request.session['administrator_id'] = login_user
                return render(request, "administrator_member_list.html", locals())
            else:
                return render(request, 'administrator_error_adm.html')
        else:
            return render(request, 'administrator_error_stu.html')

def administrator_studentlist(request):    #考试成绩界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    student_info = Person.objects.filter(userType=3).values('userId','passWord').distinct()
    user_info = Person.objects.all().values('userId','passWord','userName')

    contact_list = user_info
    paginator = Paginator(contact_list, 10)  # 每页10条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "administrator_studentlist.html", locals())

def administrator_student_details(request):    #在线考试待考课程列表界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    student_id = request.GET.get('userId')
    student_info = Person.objects.filter(userId=student_id)
    return render(request, "administrator_student_details.html", locals())

def administrator_forum_Qmanage(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    user_id = request.GET.get('userId')
    user_info = Person.objects.filter(userId=user_id)
    get_course_id = ForumQuestion.objects.filter(questionId=user_id).values('courseId').distinct()
    course_info = Course.objects.all()
    get_forum_q = ForumQuestion.objects.filter(questionId=user_id).values('courseId', 'postId', 'title', 'postTime','answerNum')
    return render(request, "administrator_forum_Qmanage.html", locals())

def administrator_forum_Amanage(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    user_id = request.GET.get('userId')
    user_info = Person.objects.filter(userId=user_id)
    get_post_id = ForumAnswer.objects.filter(answerId=user_id).values('postId', 'courseId').distinct
    get_course_id = ForumAnswer.objects.filter(answerId=user_id).values('courseId').distinct()
    course_info = Course.objects.all()
    get_forum_a = ForumAnswer.objects.filter(answerId=user_id).values('postId', 'content', 'answerTime')
    get_forum_q = ForumQuestion.objects.filter(questionId=user_id).values('courseId', 'postId', 'title')
    return render(request, "administrator_forum_Amanage.html", locals())

def administrator_courselist_stu(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    student_id = request.GET.get('userId')
    student_info = Person.objects.filter(userId=student_id)
    get_course_id = CourseStudent.objects.filter(studentId=student_id).values('courseId')
    course_info = Course.objects.all().values('courseId','courseName')

    contact_list = get_course_id
    paginator = Paginator(contact_list, 10)  # 每页10条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "administrator_courselist_stu.html", locals())

def administrator_student_grades(request):    #在线考试待考课程列表界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    student_id = request.GET.get('userId')
    course_id = request.GET.get('courseId')
    student_info = Person.objects.filter(userId=student_id).values('userId', 'userName')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    get_exam_info = Exam.objects.filter(studentId=student_id, courseId=course_id).values('courseId', 'type', 'weight', 'isOver', 'start_time', 'score')
    return render(request, "administrator_student_grades.html", locals())

def administrator_teacherlist(request):    #考试成绩界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    teacher_info = Person.objects.filter(userType=2).values('userId').distinct()
    user_info = Person.objects.all().values('userId', 'userName')

    contact_list = user_info
    paginator = Paginator(contact_list, 10)  # 每页10条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "administrator_teacherlist.html",locals())

def administrator_teacher_details(request):    #在线考试待考课程列表界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    teacher_id = request.GET.get('userId')
    teacher_info = Person.objects.filter(userId=teacher_id)
    return render(request, "administrator_teacher_details.html", locals())

def administrator_courselist_tea(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    teacher_id = request.GET.get('userId')
    teacher_info = Person.objects.filter(userId=teacher_id)
    get_course_id = Course.objects.filter(teacherId=teacher_id).values('courseId')
    course_info = Course.objects.all().values('courseId','courseName')

    contact_list = get_course_id
    paginator = Paginator(contact_list, 10)  # 每页10条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "administrator_courselist_tea.html", locals())

def administrator_course_student(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    teacher_id = request.GET.get('userId')
    course_id = request.GET.get('courseId')
    teacher_info = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    get_student_id = CourseStudent.objects.filter(courseId=course_id).values('studentId')
    get_student_grade = Grade.objects.filter(courseId=course_id).values('studentId', 'grade', 'isPass')
    student_info = Person.objects.all().values('userId', 'userName')

    contact_list = get_student_id
    paginator = Paginator(contact_list, 10)  # 每页10条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "administrator_course_student.html", locals())

def administrator_student_grades_tea(request):    #在线考试待考课程列表界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    student_id = request.GET.get('userId')
    course_id = request.GET.get('courseId')
    student_info = Person.objects.filter(userId=student_id).values('userId', 'userName')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'teacherId')
    get_exam_info = Exam.objects.filter(studentId=student_id, courseId=course_id).values('courseId', 'type', 'weight', 'isOver', 'start_time', 'score')
    return render(request, "administrator_student_grades_tea.html", locals())

def administrator_init_password(request):    #考试成绩界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userName')
    user_id = request.GET.get('userId')
    Person.objects.filter(userId=user_id).update(passWord=123456)
    return render(request, "administrator_init_password.html", locals())

def administrator_member_added(request):    #考试成绩界面
    return render(request, "administrator_member_added.html", locals())

def administrator_test_list(request):    #在线考试待考课程列表界面
    return render(request, "administrator_test_list.html")

def administrator_question_list(request):    #在线考试待考课程列表界面
    return render(request, "administrator_question_list.html")

def administrator_feedback(request):    #在线考试待考课程列表界面
    return render(request, "administrator_feedback.html")

def administrator_test_list_finished(request):    #已通过成绩页面
    return render(request, "administrator_test_list_finished.html", locals())

def administrator_test_list_unfinished(request):    #未通过成绩界面
    return render(request, "administrator_test_list_unfinished.html", locals())



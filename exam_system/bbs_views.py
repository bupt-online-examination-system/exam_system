from django.shortcuts import render
from.models import *
from django.db.models import Q
from django.db.models.aggregates import Count
from datetime import datetime

from django.contrib.auth.decorators import login_required
import time

# import pandas
from graduation_project import settings
from django.http import HttpResponse


#@login_required
#python的装饰器，相当于java中的注解     @login_required表示必须登录才能访问，否则跳转到登录页面，在settings.py中配置LGOIN_URL参数（即登陆url）
def event_manage(request):
    userId = request.GET.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    request.session['userId'] = userId
    course_info=Course.objects.all() #全部用 all，部分条件用filter
    return render(request, "guest_manage.html", locals())

def course_forum(request):
    userId = request.session.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    courseId = request.GET.get("courseId")
    if request.method == "GET":
        post_question_info = ForumQuestion.objects.filter(courseId=courseId)
        return render(request, "course_forum.html",locals())
    elif request.method == "POST":
        # userId = request.session.get('userId')
        # userName = request.session.get('userName')
        # courseId = request.GET.get("courseId")
        # post_question_info = ForumQuestion.objects.filter(courseId=courseId)
        keyword = request.POST.get('message')
        post_question_info = ForumQuestion.objects.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword)|Q(title__icontains=keyword))
        return render(request, "course_forum.html", locals())

def course_post(request):
    userId = request.session.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    postId = request.GET.get("postId")
    courseId = request.GET.get("courseId")
    post_question_info = ForumQuestion.objects.filter(postId=postId).values('postId', 'questionId', 'courseId', 'content', 'title',)
    post_answer_info = ForumAnswer.objects.filter(postId_id=postId).values('postId', 'answerId', 'content')
    user_info = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    # answer_post_info = Person.objects.filter(userId=course_post_info.answerId)
    return render(request, "course_post.html", locals())

def new_post(request):
    if request.method == "GET":
        return render(request, "new_post.html")
    elif request.method == "POST":
        userId = request.session.get('userId')
        userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
        courseId = request.GET.get("courseId")
        subject = request.POST.get('subject','无标题')
        message = request.POST.get('message','无内容')
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newPostTime = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
        ForumQuestion.objects.create(content=message,title=subject,courseId_id=courseId,postTime=newPostTime,questionId_id=userId)
        post_question_info = ForumQuestion.objects.filter(courseId=courseId)
        # bug 返回时会重新插入一遍数据
        return render(request, "course_forum.html",locals())

def edit_post(request):
    if request.method == "GET":
        return render(request, "edit_post.html")
    elif request.method == "POST":
        userId = request.session.get('userId')
        userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
        postId = request.GET.get("postId")
        courseId = request.GET.get("courseId")
        subject = request.POST.get('subject','无标题')
        message = request.POST.get('message','无内容')
        ForumQuestion.objects.filter(postId=postId).update(content=message, title=subject)
        post_question_info = ForumQuestion.objects.filter(postId=postId)
        post_answer_info = ForumAnswer.objects.filter(postId_id=postId)

        return render(request, "course_post.html", locals())

def delete_post(request):
    userId = request.session.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    postId = request.GET.get("postId")
    courseId = request.GET.get("courseId")
    ForumQuestion.objects.filter(postId=postId).delete()
    ForumAnswer.objects.filter(postId_id=postId).delete()
    post_question_info = ForumQuestion.objects.filter(courseId=courseId)

    return render(request, "course_forum.html", locals())

def answer_post(request):
    userId = request.session.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    postId = request.GET.get("postId")
    courseId = request.GET.get("courseId")
    if request.method == "GET":
        return render(request, "answer_post.html")
    elif request.method == "POST":
        message = request.POST.get('message','无内容')
        ForumAnswer.objects.create(content=message,answerId_id=userId,postId_id=postId)
        post_question_info = ForumQuestion.objects.filter(postId=postId)
        post_answer_info = ForumAnswer.objects.filter(postId_id=postId)
        # bug 返回时会重新插入一遍数据 刷新网页也会多添加一次数据

        return render(request, "course_post.html", locals())

def top_post(request):
    userId = request.session.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    postId = request.GET.get("postId")
    courseId = request.GET.get("courseId")
    post_question_top_info = ForumQuestion.objects.filter(postId=postId)
    post_question_info = ForumQuestion.objects.filter(~Q(postId=postId))

    return render(request, "course_forum.html",locals())


def stop_top_post(request):
    userId = request.session.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    courseId = request.GET.get("courseId")
    post_question_info = ForumQuestion.objects.filter(courseId=courseId)
    return render(request, "course_forum.html", locals())

def count(request):
    userId = request.session.get('userId')
    userName = Person.objects.filter(userId=userId).values('userId', 'userType', 'userName')
    count_course_info = Course.objects.values('courseId','courseName').annotate(course_id=Count('courseId'))
    count_answer_info = ForumQuestion.objects.all()
    #count_question_info = ForumQuestion.objects.annotate(count('courseId'))
    # count_answer_info = ForumAnswer.objects.annotate(count('courseId'))
    return render(request, "count.html", locals())
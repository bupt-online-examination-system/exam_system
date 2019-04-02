"""exam_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from exam_system import tools_views, adminstrator_views
from exam_system import bbs_views
from exam_system import student_views
from exam_system import teacher_views
from . import settings
from django.views.static import serve

from django.conf.urls.static import static
#使用其他模块的东西要先import      as tool_views是为了区分不同模块的views
urlpatterns = [
    url(r'^start_exam/$', tools_views.start_exam, name='start_exam'),
    url(r'^get_psw/$', tools_views.get_psw, name='get_psw'),

    # 论坛模块
    url(r'^event_manage/$', bbs_views.event_manage, name='event_manage'),
    url(r'^course_forum/$', bbs_views.course_forum, name='course_forum'),
    url(r'^course_post/$', bbs_views.course_post, name='course_post'),
    url(r'^new_post/$', bbs_views.new_post, name='new_post'),
    url(r'^edit_post/$', bbs_views.edit_post, name='edit_post'),
    url(r'^delete_post/$', bbs_views.delete_post, name='delete_post'),
    url(r'^answer_post/$', bbs_views.answer_post, name='answer_post'),
    url(r'^top_post/$', bbs_views.top_post, name='top_post'),
    url(r'^stop_top_post/$', bbs_views.stop_top_post, name='stop_top_post'),
    url(r'^count/$', bbs_views.count, name='count'),

    #name=xxx是为了在html中直接引用，例如href="/xxx/"   替代了href="127.0.0.1/xxx/"
    url(r'^file/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^send_email/$', tools_views.send_email, name='send_email'),
    url(r'^data_in/$', tools_views.data_in, name='data_in'),
    url(r'^data_out/$', tools_views.data_out, name='data_out'),
    # url(r'^ajax/post/', tools_views.ajax_post,name='ajax/post'),

    #学生模块
    url(r'^student_login/$', student_views.student_login, name='student_login'),
    url(r'^exam_list/$', student_views.exam_list, name='exam_list'),
    url(r'^practice_list/$', student_views.practice_list, name='practice_list'),
    url(r'^personal_homepage/$', student_views.personal_homepage, name='personal_homepage'),
    url(r'^score_query/$', student_views.score_query, name='score_query'),
    url(r'^pass_score_query/$', student_views.pass_score_query, name='pass_score_query'),
    url(r'^fail_score_query/$', student_views.fail_score_query, name='fail_score_query'),
    url(r'^exam_details/$', student_views.exam_details, name='exam_details'),

    #管理员模块
    url(r'^administrator_login/$', adminstrator_views.adminstrator_login, name='adminstrator_login'),
    url(r'^student_list/$', adminstrator_views.student_list, name='student_list'),
    url(r'^teacher_list/$', adminstrator_views.teacher_list, name='teacher_list'),
    
    url(r'^question_list/$', adminstrator_views.question_list, name='question_list'),

    # 教师模块
    url(r'^teacher_login/$', teacher_views.teacher_login, name='teacher_login'),
    url(r'^student_name/$', teacher_views.teacher_login, name='student_name'),
    url(r'^exam_specification/$', teacher_views.teacher_login, name='exam_specification'),
    url(r'^teacher_homepage/$', teacher_views.teacher_login, name='teacher_homepage'),
    url(r'^student_detail/$', teacher_views.teacher_login, name='student_detail'),
    url(r'^all_student/$', teacher_views.teacher_login, name='all_student'),
    url(r'^question_added/$', teacher_views.teacher_login, name='question_added'),
]
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  这种方法仅仅在debug模式下起作用


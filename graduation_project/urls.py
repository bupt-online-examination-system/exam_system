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
from exam_system import tools_views, administrator_views
from exam_system import bbs_views
from exam_system import student_views
from exam_system import teacher_views
from . import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views
from exam_system import administrator_views


from django.conf.urls.static import static
#使用其他模块的东西要先import      as tool_views是为了区分不同模块的views
from django.conf.urls import url, include
from django.contrib import admin
urlpatterns = [
#     # url(r'^start_exam/$', tools_views.start_exam, name='start_exam'),




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

    #工具模块
    url(r'^reset_psw/$', tools_views.reset_psw, name='reset_psw'),
    url(r'^file/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^send_email/$', tools_views.send_email, name='send_email'),
    url(r'^data_in/$', tools_views.data_in, name='data_in'),
    url(r'^data_out/$', tools_views.data_out, name='data_out'),
    url(r'^exam_details/ajax/post/$', tools_views.ajax_post,name='ajax/post'),

    #学生模块
    url(r'^student_login/$', student_views.student_login, name='student_login'),
    url(r'^exam_list/$', student_views.exam_list, name='exam_list'),
    url(r'^practice_list/$', student_views.practice_list, name='practice_list'),
    url(r'^mistake_list/$', student_views.mistake_list, name='mistake_list'),
    url(r'^practice_choice/$', student_views.practice_choice, name='practice_choice'),
    url(r'^practice_fill/$', student_views.practice_fill, name='practice_fill'),
    url(r'^mistake_choice/$', student_views.mistake_choice, name='mistake_choice'),
    url(r'^mistake_fill/$', student_views.mistake_fill, name='mistake_fill'),
    url(r'^practice_choice_details/$', student_views.practice_choice_details, name='practice_choice_details'),
    url(r'^practice_choice_details_answer/$', student_views.practice_choice_details_answer, name='practice_choice_details_answer'),
    url(r'^practice_fill_details/$', student_views.practice_fill_details, name='practice_fill_details'),
    url(r'^practice_fill_details_answer/$', student_views.practice_fill_details_answer, name='practice_fill_details_answer'),
    url(r'^mistake_choice_details/$', student_views.mistake_choice_details, name='mistake_choice_details'),
    url(r'^mistake_choice_details_answer/$', student_views.mistake_choice_details_answer,name='mistake_choice_details_answer'),
    url(r'^mistake_fill_details/$', student_views.mistake_fill_details, name='mistake_fill_details'),
    url(r'^mistake_fill_details_answer/$', student_views.mistake_fill_details_answer,name='mistake_fill_details_answer'),
    url(r'^exam_details/$', tools_views.exam_details, name='exam_details'),
    url(r'^personal_homepage/$', student_views.personal_homepage, name='personal_homepage'),
    url(r'^score_query/$', student_views.score_query, name='score_query'),
    url(r'^pass_score_query/$', student_views.pass_score_query, name='pass_score_query'),
    url(r'^fail_score_query/$', student_views.fail_score_query, name='fail_score_query'),
    url(r'^pass_exam_details/$', student_views.pass_exam_details, name='pass_exam_details'),
    url(r'^fail_exam_details/$', student_views.fail_exam_details, name='fail_exam_details'),
    url(r'^exam_schedule/$', student_views.exam_schedule, name='exam_schedule'),
    url(r'^exam_schedule_details/$', student_views.exam_schedule_details, name='schedule_exam_details'),
    url(r'^post_record/$', student_views.post_record, name='post_record'),

    #管理员模块
    url(r'^index/$', administrator_views.index, name='index'),
    url(r'^administrator_login/$', administrator_views.administrator_login, name='administrator_login'),
    url(r'^administrator_member_list/$', administrator_views.administrator_member_list, name='administrator_member_list'),
    url(r'^administrator_test_manage/$', administrator_views.administrator_test_manage, name='administrator_test_manage'),
    url(r'^administrator_question_list/$', administrator_views.administrator_question_list, name='administrator_question_list'),
    url(r'^administrator_forum_Qmanage/$', administrator_views.administrator_forum_Qmanage, name='administrator_forum_Qmanage'),
    url(r'^administrator_forum_Amanage/$', administrator_views.administrator_forum_Amanage, name='administrator_forum_Amanage'),
    url(r'^administrator_forum_A_delete/$', administrator_views.administrator_forum_A_delete, name='administrator_forum_A_delete'),
    url(r'^administrator_forum_Q_delete/$', administrator_views.administrator_forum_Q_delete, name='administrator_forum_Q_delete'),
    url(r'^administrator_forum_A_delete_succeed/$', administrator_views.administrator_forum_A_delete_succeed, name='administrator_forum_A_delete_succeed'),
    url(r'^administrator_forum_Q_delete_succeed/$', administrator_views.administrator_forum_Q_delete_succeed, name='administrator_forum_Q_delete_succeed'),
    url(r'^administrator_feedback/$', administrator_views.administrator_feedback, name='administrator_feedback'),
    url(r'^administrator_studentlist/$', administrator_views.administrator_studentlist, name='administrator_studentlist'),
    url(r'^administrator_teacherlist/$', administrator_views.administrator_teacherlist, name='administrator_teacherlist'),
    url(r'^administrator_exam_Q/$', administrator_views.administrator_exam_Q, name='administrator_exam_Q'),
    url(r'^administrator_C_edit/$', administrator_views.administrator_C_edit, name='administrator_C_edit'),
    url(r'^administrator_C_delete/$', administrator_views.administrator_C_delete, name='administrator_C_delete'),
    url(r'^administrator_F_edit/$', administrator_views.administrator_F_edit, name='administrator_F_edit'),
    url(r'^administrator_F_delete/$', administrator_views.administrator_F_delete, name='administrator_F_delete'),
    url(r'^administrator_C_delete_succeed/$', administrator_views.administrator_C_delete_succeed, name='administrator_C_delete_succeed'),
    url(r'^administrator_C_edit_succeed/$', administrator_views.administrator_C_edit_succeed, name='administrator_C_edit_succeed'),
    url(r'^administrator_F_delete_succeed/$', administrator_views.administrator_F_delete_succeed, name='administrator_F_delete_succeed'),
    url(r'^administrator_F_edit_succeed/$', administrator_views.administrator_F_edit_succeed, name='administrator_F_edit_succeed'),
    url(r'^administrator_question_failed_page/$', administrator_views.administrator_failed_page, name='administrator_failed_page'),
    url(r'^administrator_exam_grade/$', administrator_views.administrator_exam_grade, name='administrator_exam_grade'),
    url(r'^测试/$', administrator_views.test, name='测试'),
    url(r'^administrator_index_stu/$', administrator_views.administrator_index_stu, name='administrator_index_stu'),
    url(r'^administrator_index_tea/$', administrator_views.administrator_index_tea, name='administrator_index_tea'),
    url(r'^administrator_index_adm/$', administrator_views.administrator_index_adm, name='administrator_index_adm'),
    url(r'^administrator_error_stu/$', administrator_views.administrator_error_stu, name='administrator_error_stu'),
    url(r'^administrator_error_adm/$', administrator_views.administrator_error_adm, name='administrator_error_adm'),
    url(r'^administrator_error_tea/$', administrator_views.administrator_error_tea, name='administrator_error_tea'),
    url(r'^administrator_member_added/$', administrator_views.administrator_member_added, name='administrator_member_added'),
    url(r'^administrator_student_details/$', administrator_views.administrator_student_details, name='administrator_student_details'),
    url(r'^administrator_teacher_details/$', administrator_views.administrator_teacher_details, name='administrator_teacher_details'),
    url(r'^administrator_courselist_stu/$', administrator_views.administrator_courselist_stu, name='administrator_courselist_stu'),
    url(r'^administrator_courselist_tea/$', administrator_views.administrator_courselist_tea, name='administrator_courselist_tea'),
    url(r'^administrator_student_grades/$', administrator_views.administrator_student_grades, name='administrator_student_grades'),
    url(r'^administrator_student_grades_tea/$', administrator_views.administrator_student_grades_tea, name='administrator_student_grades_tea'),
    url(r'^administrator_course_student/$', administrator_views.administrator_course_student, name='administrator_course_student'),
    url(r'^administrator_init_password/$', administrator_views.administrator_init_password, name='administrator_init_password'),

    # 教师模块
    url(r'^teacher_login/$', teacher_views.teacher_login, name='teacher_login'),
    url(r'^student_name/$', teacher_views.student_name, name='student_name'),
    url(r'^exam_specification/$', teacher_views.exam_specification, name='exam_specification'),
    url(r'^teacher_homepage/$', teacher_views.teacher_homepage, name='teacher_homepage'),
    url(r'^student_detail1/$', teacher_views.student_detail1, name='student_detail1'),
    url(r'^student_detail2/$', teacher_views.student_detail2, name='student_detail2'),
    url(r'^student_detail3/$', teacher_views.student_detail3, name='student_detail3'),
    url(r'^student_detail4/$', teacher_views.student_detail4, name='student_detail4'),
    url(r'^all_student/$', teacher_views.all_student, name='all_student'),
    url(r'^question_added/$', teacher_views.question_added, name='question_added'),
    url(r'^course_name/$', teacher_views.course_name, name='course_name'),
    url(r'^exam_number/$', teacher_views.exam_number, name='exam_number'),
    url(r'^first_exam/$', teacher_views.first_exam, name='first_exam'),
    url(r'^second_exam/$', teacher_views.second_exam, name='second_exam'),
    url(r'^third_exam/$', teacher_views.third_exam, name='third_exam'),
    url(r'^final_exam/$', teacher_views.final_exam, name='final_exam'),
    url(r'^overall/$', teacher_views.overall, name='overall'),
    url(r'^add_course/$', teacher_views.add_course, name='add_course'),
    url(r'^add_exam/$', teacher_views.add_exam, name='add_exam'),
    url(r'^add_student/$', teacher_views.add_student, name='add_student'),
    url(r'^teacher_C_delete/$', teacher_views.teacher_C_delete, name='teacher_C_delete'),
    url(r'^teacher_F_delete/$', teacher_views.teacher_F_delete, name='teacher_F_delete'),
    url(r'^teacher_C_edit/$', teacher_views.teacher_C_edit, name='teacher_C_edit'),
    url(r'^teacher_F_edit/$', teacher_views.teacher_F_edit, name='teacher_F_edit'),
    url(r'^teacher_question_list/$', teacher_views.teacher_question_list, name='teacher_question_list'),
    url(r'^teacher_question_added/$', teacher_views.teacher_question_added, name='teacher_question_added'),
    url(r'^teacher_course/$', teacher_views.teacher_course, name='teacher_course'),
    url(r'^teacher_C_delete_succeed/$', teacher_views.teacher_C_delete_succeed, name='teacher_C_delete_succeed'),
    url(r'^teacher_C_edit_succeed/$', teacher_views.teacher_C_edit_succeed, name='teacher_C_edit_succeed'),
    url(r'^teacher_F_delete_succeed/$', teacher_views.teacher_F_delete_succeed, name='teacher_F_delete_succeed'),
    url(r'^teacher_F_edit_succeed/$', teacher_views.teacher_F_edit_succeed, name='teacher_F_eidt_succeed'),
    url(r'^teacher_post/$', teacher_views.teacher_post, name='teacher_post'),
]
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  这种方法仅仅在debug模式下起作用


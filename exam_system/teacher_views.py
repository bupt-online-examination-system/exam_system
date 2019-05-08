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

def overall(request): #总成绩界面
    teacher_id = request.session.get('teacherId')
    teacher_name = Person.objects.filter(userId=teacher_id ).values('userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName','isOver')
    grade_info = Grade.objects.filter(courseId=course_id).values('studentId','grade','isPass')
    student_info = Person.objects.all().values('userId', 'userName')

    contact_list = grade_info
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
    return render(request, "overall.html", locals())

def course_name(request):    #所授课程界面
    teacher_id = request.session.get('teacherId')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    get_course_id = Course.objects.filter(teacherId=teacher_id).values('courseId')
    course_info = Course.objects.all().values('courseId', 'courseName')

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
    return render(request, "course_name.html", locals())

def first_exam(request):    #第一次月考
    teacher_id = request.session.get('teacherId')
    teacher_name = Person.objects.filter(userId=teacher_id ).values('userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    exam_info = Exam.objects.filter(courseId=course_id,type=1).values('score','studentId','examId','isOver')
    student_info = Person.objects.all().values('userId', 'userName')

    contact_list = exam_info
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
    return render(request, "first_exam.html", locals())

def second_exam(request):    #第二次月考
    teacher_id = request.session.get('teacherId')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    exam_info = Exam.objects.filter(courseId=course_id, type=2).values('score', 'studentId','examId')
    student_info = Person.objects.all().values('userId', 'userName')

    contact_list = exam_info
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
    return render(request, "second_exam.html", locals())

def third_exam(request):    #第三次月考
    teacher_id = request.session.get('teacherId')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    exam_info = Exam.objects.filter(courseId=course_id, type=3).values('score', 'studentId','examId')
    student_info = Person.objects.all().values('userId', 'userName')

    contact_list = exam_info
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
    return render(request, "third_exam.html", locals())

def final_exam(request):    #最后一次考试
    teacher_id = request.session.get('teacherId')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    exam_info = Exam.objects.filter(courseId=course_id, type=4).values('score', 'studentId','examId')
    student_info = Person.objects.all().values('userId', 'userName')

    contact_list = exam_info
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
    return render(request, "final_exam.html", locals())

def exam_number(request):    #选择第几次考试
    teacher_id = request.session.get('teacherId')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    course_id = request.GET.get('courseId')
    get_course_name = Course.objects.filter(courseId=course_id).values('courseName')
    return render(request, "exam_number.html", locals())

def student_name(request):    #学生名单界面
    return render(request, "student_name.html")

def exam_specification(request):    #选择试卷类型界面
    return render(request, "exam_specification.html")

def teacher_homepage(request):    #教师主页界面
    if request.method == "GET":
        teacher_id = request.session.get('teacherId')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
        return render(request, "teacher_homepage.html", locals())
    elif request.method == "POST":
        login_user = request.POST.get('userId')
        login_password = request.POST.get("passWord")
        login_user_type = list(Person.objects.filter(userId=login_user).values_list('userType', flat=True))
        count = Person.objects.filter(userId=login_user).count()
        if count == 1 and login_user_type[0] == 2:
            real_password = list(Person.objects.filter(userId=login_user).values_list('passWord', flat=True))
            if login_password == real_password[0]:
                request.session['teacherId'] = login_user
                teacher_name = Person.objects.filter(userId=login_user).values('userName')
                return render(request, "teacher_homepage.html", locals())
            else:
                return render(request, 'administrator_error_tea.html')
        else:
            return render(request, 'administrator_error_tea.html')


def student_detail1(request):    #学生具体信息界面
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    student_id = request.GET.get("studentId")
    exam_id = request.GET.get('examId')
    exam_info = ExamQuestion.objects.filter(examId=exam_id).values('questionId', 'isRight','type','answer')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    choice_info = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId','content','questionA','questionB','questionC','questionD','answer')
    fill_info = FillInTheBlank.objects.filter(courseId=course_id).values('fillId','content','answer')

    contact_list = exam_info
    paginator = Paginator(contact_list, 1)  # 每页1条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "student_detail1.html", locals())

def student_detail2(request):    #学生具体信息界面
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    student_id = request.GET.get("studentId")
    exam_id = request.GET.get('examId')
    exam_info = ExamQuestion.objects.filter(examId=exam_id).values('questionId', 'isRight','type','answer')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    choice_info = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId','content','questionA','questionB','questionC','questionD','answer')
    fill_info = FillInTheBlank.objects.filter(courseId=course_id).values('fillId','content','answer')

    contact_list = exam_info
    paginator = Paginator(contact_list, 1)  # 每页1条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "student_detail2.html", locals())

def student_detail3(request):    #学生具体信息界面
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    student_id = request.GET.get("studentId")
    exam_id = request.GET.get('examId')
    exam_info = ExamQuestion.objects.filter(examId=exam_id).values('questionId', 'isRight','type','answer')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    choice_info = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId','content','questionA','questionB','questionC','questionD','answer')
    fill_info = FillInTheBlank.objects.filter(courseId=course_id).values('fillId','content','answer')

    contact_list = exam_info
    paginator = Paginator(contact_list, 1)  # 每页1条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "student_detail3.html", locals())

def student_detail4(request):    #学生具体信息界面
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userName')
    student_id = request.GET.get("studentId")
    exam_id = request.GET.get('examId')
    exam_info = ExamQuestion.objects.filter(examId=exam_id).values('questionId', 'isRight','type','answer')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    choice_info = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId','content','questionA','questionB','questionC','questionD','answer')
    fill_info = FillInTheBlank.objects.filter(courseId=course_id).values('fillId','content','answer')

    contact_list = exam_info
    paginator = Paginator(contact_list, 1)  # 每页1条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "student_detail4.html", locals())

def add_course(request):
    return render(request,"add_course.html",locals())

def all_student(request):    #全部学生成绩分析界面
    exam_id = request.GET.get('examId')
    return render(request, "all_student.html", locals())

def question_added(request):    #试题添加界面
    return render(request, "question_added.html", locals())

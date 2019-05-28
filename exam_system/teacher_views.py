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
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id ).values('userId', 'userName')
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
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
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
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
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
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    exam_info = Exam.objects.filter(courseId=course_id, type=2).values('score', 'studentId','examId','isOver')
    student_info = Person.objects.all()

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
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    exam_info = Exam.objects.filter(courseId=course_id, type=3).values('score', 'studentId','examId','isOver')
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
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    course_name = Course.objects.filter(courseId=course_id).values('courseName')
    exam_info = Exam.objects.filter(courseId=course_id, type=4).values('score', 'studentId','examId','isOver')
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
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    get_course_name = Course.objects.filter(courseId=course_id).values('courseName')
    return render(request, "exam_number.html", locals())

def student_name(request):    #学生名单界面
    return render(request, "student_name.html")

def exam_specification(request):    #选择试卷类型界面
    return render(request, "exam_specification.html")

def teacher_homepage(request):    #教师主页界面
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        return render(request, "teacher_homepage.html", locals())
    elif request.method == "POST":
        login_user = request.POST.get('userId')
        login_password = request.POST.get("passWord")
        login_user_type = list(Person.objects.filter(userId=login_user).values_list('userType', flat=True))
        count = Person.objects.filter(userId=login_user).count()
        if count == 1 and login_user_type[0] == 2:
            real_password = list(Person.objects.filter(userId=login_user).values_list('passWord', flat=True))
            if login_password == real_password[0]:
                request.session['teacher_id'] = login_user
                teacher_name = Person.objects.filter(userId=login_user).values('userId', 'userName')
                return render(request, "teacher_homepage.html", locals())
            else:
                return render(request, 'administrator_error_tea.html')
        else:
            return render(request, 'administrator_error_tea.html')


def student_detail1(request):    #学生具体信息界面
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
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
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
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
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
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
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
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
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        get_course_list = Course.objects.filter(teacherId=teacher_id).values('courseId', 'courseName', 'isOver')

        contact_list = get_course_list
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
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_name = request.POST.get('course')
        Course.objects.create(courseName=course_name, teacherId_id=teacher_id, isOver=1)
        course_id = Course.objects.filter(courseName=course_name).values_list('courseId', flat=True)[0]
        Test.objects.create(courseId_id=course_id, isReady=1, type=1, weight=0)
        Test.objects.create(courseId_id=course_id, isReady=1, type=2, weight=0)
        Test.objects.create(courseId_id=course_id, isReady=1, type=3, weight=0)
        Test.objects.create(courseId_id=course_id, isReady=1, type=4, weight=0)
        Test.objects.create(courseId_id=course_id, isReady=1, type=5, weight=0)
        get_course_list = Course.objects.filter(teacherId=teacher_id).values('courseId', 'courseName', 'isOver')

        contact_list = get_course_list
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
    return render(request, "add_course.html", locals())

def course_end(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    Course.objects.filter(courseId=course_id).update(isOver=2)
    get_course_list = Course.objects.filter(teacherId=teacher_id).values('courseId', 'courseName', 'isOver')

    contact_list = get_course_list
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
    return render(request, "add_course.html", locals())

def delete_course(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    exist = CourseStudent.objects.filter(courseId=course_id).count()
    if exist == 0:
        Test.objects.filter(courseId=course_id).delete()
        Course.objects.filter(courseId=course_id).delete()
    get_course_list = Course.objects.filter(teacherId=teacher_id).values('courseId', 'courseName', 'isOver')

    contact_list = get_course_list
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
    return render(request, "add_course.html", locals())

def add_student(request):
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_student_id = CourseStudent.objects.filter(courseId=course_id).values('studentId')
        student_info = Person.objects.filter(userType=3).values('userId', 'userName', 'userType')

        contact_list = get_student_id
        paginator = Paginator(contact_list, 30)  # 每页10条

        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        student_id = request.POST.get('id')
        course_id = request.GET.get('courseId')
        get_student_info = Person.objects.filter(userType=3)
        is_student = Person.objects.filter(userId=student_id, userType=3).count()
        if is_student == 1:
            CourseStudent.objects.create(courseId_id=course_id, studentId_id=student_id)
        get_student_id = CourseStudent.objects.filter(courseId=course_id).values('studentId')
        student_info = Person.objects.filter(userType=3).values('userId', 'userName', 'userType')

        contact_list = get_student_id
        paginator = Paginator(contact_list, 30)  # 每页10条

        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
    return render(request, "add_student.html", locals())

def add_exam(request):
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        test_info = Test.objects.filter(courseId=course_id).values('weight', 'type', 'isReady')
        get_state_1 = Test.objects.filter(courseId=course_id, type=1).values_list('isReady', flat=True)[0]
        get_state_2 = Test.objects.filter(courseId=course_id, type=2).values_list('isReady', flat=True)[0]
        get_state_3 = Test.objects.filter(courseId=course_id, type=3).values_list('isReady', flat=True)[0]
        get_state_4 = Test.objects.filter(courseId=course_id, type=4).values_list('isReady', flat=True)[0]
        get_state_5 = Test.objects.filter(courseId=course_id, type=5).values_list('isReady', flat=True)[0]
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_state_1 = Test.objects.filter(courseId=course_id, type=1).values_list('isReady', flat=True)[0]
        get_state_2 = Test.objects.filter(courseId=course_id, type=2).values_list('isReady', flat=True)[0]
        get_state_3 = Test.objects.filter(courseId=course_id, type=3).values_list('isReady', flat=True)[0]
        get_state_4 = Test.objects.filter(courseId=course_id, type=4).values_list('isReady', flat=True)[0]
        get_state_5 = Test.objects.filter(courseId=course_id, type=5).values_list('isReady', flat=True)[0]
        weight_1 = request.POST.get('weight1')
        weight_2 = request.POST.get('weight2')
        weight_3 = request.POST.get('weight3')
        weight_4 = request.POST.get('weight4')
        if weight_1 is not None:
            Test.objects.filter(courseId=course_id, type=1).update(weight=weight_1)
        if weight_2 is not None:
            Test.objects.filter(courseId=course_id, type=2).update(weight=weight_2)
        if weight_3 is not None:
            Test.objects.filter(courseId=course_id, type=3).update(weight=weight_3)
        if weight_4 is not None:
            Test.objects.filter(courseId=course_id, type=4).update(weight=weight_4)
        test_info = Test.objects.filter(courseId=course_id).values('weight', 'type', 'isReady')
    return render(request, "add_exam.html", locals())

def test_ready(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    get_type = request.GET.get('type')
    Test.objects.filter(courseId=course_id, type=get_type).update(isReady=2)
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
    test_info = Test.objects.filter(courseId=course_id).values('weight', 'type', 'isReady')
    get_state_1 = Test.objects.filter(courseId=course_id, type=1).values_list('isReady', flat=True)[0]
    get_state_2 = Test.objects.filter(courseId=course_id, type=2).values_list('isReady', flat=True)[0]
    get_state_3 = Test.objects.filter(courseId=course_id, type=3).values_list('isReady', flat=True)[0]
    get_state_4 = Test.objects.filter(courseId=course_id, type=4).values_list('isReady', flat=True)[0]
    get_state_5 = Test.objects.filter(courseId=course_id, type=5).values_list('isReady', flat=True)[0]
    return render(request, "add_exam.html", locals())

def exam_Q(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    get_type = request.GET.get('type')
    test_info = Test.objects.filter(courseId=course_id, type=get_type).values('type', 'weight')
    test_id = Test.objects.filter(courseId=course_id, type=get_type).values_list('testId', flat=True)[0]
    print(test_id)
    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                       'questionB', 'questionC', 'questionD',
                                                                       'type')

    get_Q_id = TestQuestion.objects.filter(testId=test_id).values('questionId', 'type')
    return render(request, "exam_Q.html", locals())

def first_exam_edit(request):
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_weight = Test.objects.filter(courseId=course_id, type=1).values_list('weight', flat=True)[0]
        get_test_id = Test.objects.filter(courseId=course_id, type=1).values_list('testId', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type')
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_f_id = request.POST.get('F_id')
        get_c_id = request.POST.get('C_id')
        print(get_c_id)
        print(get_f_id)
        change_weight = request.POST.get('weight')
        get_test_id = Test.objects.filter(courseId=course_id, type=1).values_list('testId', flat=True)[0]
        if get_f_id is not None:
            f_exist = FillInTheBlank.objects.filter(courseId=course_id, type=1, fillId=get_f_id).count()
            print(f_exist)
            if f_exist == 1:
                exist_f = TestQuestion.objects.filter(questionId=get_f_id, type=2).count()
                if exist_f == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=1, questionId=get_f_id)
        if get_c_id is not None:
            c_exist = ChoiceQuestion.objects.filter(courseId=course_id, type=1, choiceId=get_c_id).count()
            print(c_exist)
            if c_exist == 1:
                exist_c = TestQuestion.objects.filter(questionId=get_c_id, type=1).count()
                if exist_c == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=1, questionId=get_c_id)
        if change_weight is not None:
            Test.objects.filter(courseId=course_id, type=1).update(weight=change_weight)
        get_weight = Test.objects.filter(courseId=course_id, type=1).values_list('weight', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type', 'courseId')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type', 'courseId')
    return render(request, "first_exam_edit.html", locals())

def second_exam_edit(request):
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_weight = Test.objects.filter(courseId=course_id, type=2).values_list('weight', flat=True)[0]
        get_test_id = Test.objects.filter(courseId=course_id, type=2).values_list('testId', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type')
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_f_id = request.POST.get('F_id')
        get_c_id = request.POST.get('C_id')
        change_weight = request.POST.get('weight')
        get_test_id = Test.objects.filter(courseId=course_id, type=2).values_list('testId', flat=True)[0]
        if get_f_id is not None:
            f_exist = FillInTheBlank.objects.filter(courseId=course_id, type=1, fillId=get_f_id).count()
            if f_exist == 1:
                exist_f = TestQuestion.objects.filter(questionId=get_f_id, type=2).count()
                if exist_f == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=2, questionId=get_f_id)
        if get_c_id is not None:
            c_exist = ChoiceQuestion.objects.filter(courseId=course_id, type=1, choiceId=get_c_id).count()
            if c_exist == 1:
                exist_c = TestQuestion.objects.filter(questionId=get_c_id, type=1).count()
                if exist_c == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=1, questionId=get_c_id)
        if change_weight is not None:
            Test.objects.filter(courseId=course_id, type=2).update(weight=change_weight)
        get_weight = Test.objects.filter(courseId=course_id, type=2).values_list('weight', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type', 'courseId')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type', 'courseId')
    return render(request, "second_exam_edit.html", locals())

def third_exam_edit(request):
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_weight = Test.objects.filter(courseId=course_id, type=3).values_list('weight', flat=True)[0]
        get_test_id = Test.objects.filter(courseId=course_id, type=3).values_list('testId', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type')
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_f_id = request.POST.get('F_id')
        get_c_id = request.POST.get('C_id')
        print(get_c_id)
        print(get_f_id)
        change_weight = request.POST.get('weight')
        get_test_id = Test.objects.filter(courseId=course_id, type=3).values_list('testId', flat=True)[0]
        if get_f_id is not None:
            f_exist = FillInTheBlank.objects.filter(courseId=course_id, type=1, fillId=get_f_id).count()
            print(f_exist)
            if f_exist == 1:
                exist_f = TestQuestion.objects.filter(questionId=get_f_id, type=2).count()
                if exist_f == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=2, questionId=get_f_id)
        if get_c_id is not None:
            c_exist = ChoiceQuestion.objects.filter(courseId=course_id, type=1, choiceId=get_c_id).count()
            print(c_exist)
            if c_exist == 1:
                exist_c = TestQuestion.objects.filter(questionId=get_c_id, type=1).count()
                if exist_c == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=1, questionId=get_c_id)
        if change_weight is not None:
            Test.objects.filter(courseId=course_id, type=3).update(weight=change_weight)
        get_weight = Test.objects.filter(courseId=course_id, type=3).values_list('weight', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type', 'courseId')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type', 'courseId')
    return render(request, "third_exam_edit.html", locals())

def final_exam_edit(request):
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_weight = Test.objects.filter(courseId=course_id, type=4).values_list('weight', flat=True)[0]
        get_test_id = Test.objects.filter(courseId=course_id, type=4).values_list('testId', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type')
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_f_id = request.POST.get('F_id')
        get_c_id = request.POST.get('C_id')
        change_weight = request.POST.get('weight')
        get_test_id = Test.objects.filter(courseId=course_id, type=4).values_list('testId', flat=True)[0]
        if get_f_id is not None:
            f_exist = FillInTheBlank.objects.filter(courseId=course_id, type=1, fillId=get_f_id).count()
            print(f_exist)
            if f_exist == 1:
                exist_f = TestQuestion.objects.filter(questionId=get_f_id, type=2).count()
                if exist_f == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=2, questionId=get_f_id)
        if get_c_id is not None:
            c_exist = ChoiceQuestion.objects.filter(courseId=course_id, type=1, choiceId=get_c_id).count()
            print(c_exist)
            if c_exist == 1:
                exist_c = TestQuestion.objects.filter(questionId=get_c_id, type=1).count()
                if exist_c == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=1, questionId=get_c_id)
        if change_weight is not None:
            Test.objects.filter(courseId=course_id, type=4).update(weight=change_weight)
        get_weight = Test.objects.filter(courseId=course_id, type=4).values_list('weight', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type', 'courseId')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type', 'courseId')
    return render(request, "final_exam_edit.html", locals())

def practice_edit(request):
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_weight = Test.objects.filter(courseId=course_id, type=5).values_list('weight', flat=True)[0]
        get_test_id = Test.objects.filter(courseId=course_id, type=5).values_list('testId', flat=True)[0]
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type')
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
        get_f_id = request.POST.get('F_id')
        get_c_id = request.POST.get('C_id')
        print(get_c_id)
        print(get_f_id)
        get_test_id = Test.objects.filter(courseId=course_id, type=2).values_list('testId', flat=True)[0]
        if get_f_id is not None:
            f_exist = FillInTheBlank.objects.filter(courseId=course_id, type=2, fillId=get_f_id).count()
            print(f_exist)
            if f_exist == 1:
                exist_f = TestQuestion.objects.filter(questionId=get_f_id, type=2).count()
                if exist_f == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=2, questionId=get_f_id)
        if get_c_id is not None:
            c_exist = ChoiceQuestion.objects.filter(courseId=course_id, type=2, choiceId=get_c_id).count()
            print(c_exist)
            if c_exist == 1:
                exist_c = TestQuestion.objects.filter(questionId=get_c_id, type=1).count()
                if exist_c == 0:
                    TestQuestion.objects.create(testId_id=get_test_id, type=1, questionId=get_c_id)
        get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type', 'courseId')
        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                           'questionB', 'questionC', 'questionD',
                                                                           'type', 'courseId')
    return render(request, "practice_edit.html", locals())

def delete_Q_1(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    q_id = request.GET.get('questionId')
    get_type = request.GET.get('type')
    course_id = request.GET.get('courseId')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
    get_weight = Test.objects.filter(courseId=course_id, type=1).values_list('weight', flat=True)[0]
    get_test_id = Test.objects.filter(courseId=course_id, type=1).values_list('testId', flat=True)[0]
    TestQuestion.objects.filter(testId=get_test_id, questionId=q_id, type=get_type).delete()
    get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type', 'courseId')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                       'questionB', 'questionC', 'questionD',
                                                                       'type', 'courseId')
    return render(request, "first_exam_edit.html", locals())

def delete_Q_2(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    q_id = request.GET.get('questionId')
    get_type = request.GET.get('type')
    course_id = request.GET.get('courseId')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
    get_weight = Test.objects.filter(courseId=course_id, type=2).values_list('weight', flat=True)[0]
    get_test_id = Test.objects.filter(courseId=course_id, type=2).values_list('testId', flat=True)[0]
    TestQuestion.objects.filter(testId=get_test_id, questionId=q_id, type=get_type).delete()
    get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type', 'courseId')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                       'questionB', 'questionC', 'questionD',
                                                                       'type', 'courseId')
    return render(request, "second_exam_edit.html", locals())


def delete_Q_3(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    q_id = request.GET.get('questionId')
    get_type = request.GET.get('type')
    course_id = request.GET.get('courseId')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
    get_weight = Test.objects.filter(courseId=course_id, type=3).values_list('weight', flat=True)[0]
    get_test_id = Test.objects.filter(courseId=course_id, type=3).values_list('testId', flat=True)[0]
    TestQuestion.objects.filter(testId=get_test_id, questionId=q_id, type=get_type).delete()
    get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type',
                                                                       'courseId')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                       'questionB', 'questionC', 'questionD',
                                                                       'type', 'courseId')
    return render(request, "third_exam_edit.html", locals())

def delete_Q_4(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    q_id = request.GET.get('questionId')
    get_type = request.GET.get('type')
    course_id = request.GET.get('courseId')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
    get_weight = Test.objects.filter(courseId=course_id, type=4).values_list('weight', flat=True)[0]
    get_test_id = Test.objects.filter(courseId=course_id, type=4).values_list('testId', flat=True)[0]
    TestQuestion.objects.filter(testId=get_test_id, questionId=q_id, type=get_type).delete()
    get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type',
                                                                       'courseId')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                       'questionB', 'questionC', 'questionD',
                                                                       'type', 'courseId')
    return render(request, "final_exam_edit.html", locals())

def delete_Q_5(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    q_id = request.GET.get('questionId')
    get_type = request.GET.get('type')
    course_id = request.GET.get('courseId')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
    get_weight = Test.objects.filter(courseId=course_id, type=5).values_list('weight', flat=True)[0]
    get_test_id = Test.objects.filter(courseId=course_id, type=5).values_list('testId', flat=True)[0]
    TestQuestion.objects.filter(testId=get_test_id, questionId=q_id, type=get_type).delete()
    get_question_list = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')

    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type',
                                                                       'courseId')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA',
                                                                       'questionB', 'questionC', 'questionD',
                                                                       'type', 'courseId')
    return render(request, "practice_edit.html", locals())

def teacher_question_added(request):
    return render(request, "teacher_question_added.html", locals())


def teacher_question_list(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    return render(request, "teacher_question_list.html", locals())

def teacher_C_delete(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    page = request.GET.get('page')
    question_id = request.GET.get('choiceId')
    get_question_info = ChoiceQuestion.objects.filter(choiceId=question_id).values('choiceId', 'courseId', 'content',
                                                                                   'answer', 'questionA', 'questionB',
                                                                                   'questionC', 'questionD', 'type')
    course_info = Course.objects.all()
    find_question = ExamQuestion.objects.filter(questionId=question_id, type=1).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "teacher_C_delete.html", locals())


def teacher_C_delete_succeed(request):
    question_id = request.GET.get('questionId')
    ChoiceQuestion.objects.filter(choiceId=question_id).delete()
    page = request.GET.get('page')
    return render(request, "teacher_C_delete_succeed.html", locals())

def teacher_C_edit(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    question_id = request.GET.get('choiceId')
    page = request.GET.get('page')
    get_question_info = ChoiceQuestion.objects.filter(choiceId=question_id).values('choiceId', 'courseId',
                                                                                   'content',
                                                                                   'answer', 'questionA',
                                                                                   'questionB',
                                                                                   'questionC', 'questionD', 'type')
    course_info = Course.objects.all()
    find_question = ExamQuestion.objects.filter(questionId=question_id, type=1).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "teacher_C_edit.html", locals())


def teacher_C_edit_succeed(request):
    if request.method == "GET":
        return render(request, "teacher_C_edit_succeed.html", locals())
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        question_id = request.GET.get('choiceId')
        get_question_info = ChoiceQuestion.objects.filter(choiceId=question_id).values('choiceId')
        get_content = request.POST.get('content')
        page = request.GET.get('page')
        a = request.POST.get('A')
        b = request.POST.get('B')
        c = request.POST.get('C')
        d = request.POST.get('D')
        answer = request.POST.get('answer')
        get_type = request.POST.get('type')
        course_id = request.POST.get('courseId')
        ChoiceQuestion.objects.filter(choiceId=question_id).update(content=get_content, questionA=a,
                                                                   questionB=b, questionC=c,
                                                                   questionD=d, answer=answer, type=get_type,
                                                                   courseId_id=course_id)
    return render(request, "teacher_C_edit_succeed.html", locals())

def teacher_F_delete(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    page = request.GET.get('page')
    question_id = request.GET.get('fillId')
    get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId', 'courseId', 'content', 'answer', 'type')
    course_info = Course.objects.all()
    find_question = ExamQuestion.objects.filter(questionId=question_id, type=2).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "teacher_F_delete.html", locals())


def teacher_F_delete_succeed(request):
    question_id = request.GET.get('questionId')
    FillInTheBlank.objects.filter(fillId=question_id).delete()
    page = request.GET.get('page')
    return render(request, "teacher_F_delete_succeed.html", locals())

def teacher_F_edit(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    question_id = request.GET.get('fillId')
    page = request.GET.get('page')
    get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId', 'courseId', 'content',
                                                                                 'answer', 'type')
    course_info = Course.objects.all()
    find_question = ExamQuestion.objects.filter(questionId=question_id, type=2).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "teacher_F_edit.html", locals())

def teacher_F_edit_succeed(request):
    if request.method == "GET":
        return render(request, "teacher_F_edit_succeed.html", locals())
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        question_id = request.GET.get('fillId')
        get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId')
        get_content = request.POST.get('content')
        page = request.GET.get('page')
        answer = request.POST.get('answer')
        get_type = request.POST.get('type')
        course_id = request.POST.get('courseId')
        print(question_id)
        print(get_content)
        print(answer)
        print(get_type)
        print(course_id)
        FillInTheBlank.objects.filter(fillId=question_id).update(content=get_content, answer=answer, type=get_type,
                                                                 courseId_id=course_id)
    return render(request, "teacher_F_edit_succeed.html", locals())

def teacher_course(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
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
    return render(request, "teacher_course.html", locals())

def all_student(request):    #全部学生成绩分析界面
    exam_id = request.GET.get('examId')
    return render(request, "all_student.html", locals())

def question_added(request):    #试题添加界面
    return render(request, "question_added.html", locals())

def teacher_choice_list(request):    #添加选择题界面
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')

        get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id)
        contact_list = get_Q_C

        paginator = Paginator(contact_list, 5)  # 每页5条

        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        keyword = request.POST.get('choice')
        if keyword is None:
            get_content = request.POST.get('content')
            a = request.POST.get('A')
            b = request.POST.get('B')
            c = request.POST.get('C')
            d = request.POST.get('D')
            answer = request.POST.get('answer')
            get_type = request.POST.get('type')

            exist = ChoiceQuestion.objects.filter(content=get_content, type=get_type, questionA=a, questionB=b, questionC=c, questionD=d, answer=answer, courseId_id=course_id).count()
            if exist == 0:
                ChoiceQuestion.objects.create(content=get_content, questionA=a, questionB=b, questionC=c, questionD=d,answer=answer, type=get_type, courseId_id=course_id)

            course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
            get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id)
            contact_list = get_Q_C
        else:
            get_Q_C = ChoiceQuestion.objects.filter(Q(content__icontains=keyword) | Q(choiceId__icontains=keyword) | Q(questionA__contains=keyword) | Q(questionB__contains=keyword) | Q(questionC__contains=keyword) | Q(questionD__contains=keyword))
            contact_list = get_Q_C

        paginator = Paginator(contact_list, 5)  # 每页5条

        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
    return render(request, "teacher_choice_list.html", locals())


def teacher_fill_list(request):    #添加填空题界面
    if request.method == "GET":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
        get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')

        contact_list = get_Q_F
        paginator = Paginator(contact_list, 5)  # 每页5条

        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
    elif request.method == "POST":
        teacher_id = request.session.get('teacher_id')
        teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        keyword = request.POST.get('fill')
        if keyword is None:
            course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
            get_content = request.POST.get('content')
            answer = request.POST.get('answer')
            get_type = request.POST.get('type')
            FillInTheBlank.objects.create(content=get_content, answer=answer, type=get_type, courseId_id=course_id)

            get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
            contact_list = get_Q_F
        else:
            get_Q_F = FillInTheBlank.objects.filter(Q(content__icontains=keyword) | Q(fillId__icontains=keyword) |
                                                    Q(answer__icontains=keyword))
            contact_list = get_Q_F

        paginator = Paginator(contact_list, 5)  # 每页5条
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
    return render(request, "teacher_fill_list.html", locals())

def teacher_post(request):
    teacher_id = request.session.get('teacher_id')
    teacher_name = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    forum_question_info = ForumQuestion.objects.filter(questionId=teacher_id).values('title','courseId','postId')
    course_info = Course.objects.all().values('courseId','courseName')
    return render(request, "teacher_post.html", locals())


from django.shortcuts import render
from.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q

def index(request): #管理员界面模板
    request.session['administrator_id'] = ''
    request.session['teacher_id'] = ''
    request.session['studentId'] = ''
    return render(request, "index.html", locals())

def administrator_login(request):
    return render(request, "administrator_login.html")

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
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        return render(request, "administrator_member_list.html", locals())
    elif request.method == "POST":
        login_user = request.POST.get('userId')
        login_password = request.POST.get("passWord")
        login_user_type = Person.objects.filter(userId=login_user).values_list('userType', flat=True)
        administrator_name = Person.objects.filter(userId=login_user).values('userId', 'userName')
        count = Person.objects.filter(userId=login_user).count()
        if count == 1 and login_user_type[0] == 1:
            real_password = list(Person.objects.filter(userId=login_user).values_list('passWord', flat=True))
            if login_password == real_password[0]:
                request.session['administrator_id'] = login_user
                return render(request, "administrator_member_list.html", locals())
            else:
                return render(request, 'administrator_error_adm.html')
        else:
            return render(request, 'administrator_error_adm.html')

def administrator_studentlist(request):    #考试成绩界面
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        keyword = request.GET.get('keyword')
        if keyword is None:
            student_info = Person.objects.filter(userType=3)
            contact_list = student_info
        else:
            student_info = Person.objects.filter((Q(userType=3)) & (Q(userName__icontains=keyword) | Q(userId__icontains=keyword)))
            contact_list = student_info

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
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        keyword = request.POST.get('student')
        if keyword is None:
            student_id = request.POST.get('id')
            student_password = request.POST.get('password')
            student_name = request.POST.get('name')
            exist = Person.objects.filter(userId=student_id, userType=3).count()
            if exist == 0:
                Person.objects.create(userId=student_id, userType=3, userName=student_name, passWord=student_password)
            student_info = Person.objects.filter(userType=3)
            contact_list = student_info
        else:
            student_info = Person.objects.filter((Q(userType=3)) &(Q(userName__icontains=keyword) | Q(userId__icontains=keyword)))
            contact_list = student_info

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

def administrator_student_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    student_id = request.GET.get('userId')
    student_info = Person.objects.filter(userType=3)
    exist = CourseStudent.objects.filter(studentId=student_id).count()
    if exist == 0:
        Person.objects.filter(userId=student_id).delete()
    contact_list = student_info
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
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    student_id = request.GET.get('userId')
    student_info = Person.objects.filter(userId=student_id)
    return render(request, "administrator_student_details.html", locals())

def administrator_forum_Qmanage(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    user_id = request.GET.get('userId')
    user_info = Person.objects.filter(userId=user_id)
    get_course_id = ForumQuestion.objects.filter(questionId=user_id).values('courseId').distinct()
    course_info = Course.objects.all()
    get_forum_q = ForumQuestion.objects.filter(questionId=user_id).values('courseId', 'postId', 'title', 'postTime','answerNum')
    return render(request, "administrator_forum_Qmanage.html", locals())

def administrator_forum_Amanage(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    user_id = request.GET.get('userId')
    user_info = Person.objects.filter(userId=user_id)
    get_post_id = ForumAnswer.objects.filter(answerId=user_id).values('postId', 'courseId').distinct
    get_course_id = ForumAnswer.objects.filter(answerId=user_id).values('courseId').distinct()
    course_info = Course.objects.all()
    get_forum_a = ForumAnswer.objects.filter(answerId=user_id).values('postId', 'answerId', 'content', 'answerTime')
    get_forum_q = ForumQuestion.objects.filter(questionId=user_id).values('courseId', 'postId', 'title')
    return render(request, "administrator_forum_Amanage.html", locals())

def administrator_forum_Q_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_info = Course.objects.all().values('courseId', 'courseName')
    post_id = request.GET.get('postId')
    get_user_id = ForumQuestion.objects.filter(postId=post_id).values_list('questionId', flat=True)[0]
    get_course_id = ForumQuestion.objects.filter(postId=post_id).values_list('courseId', flat=True)[0]
    user_info = Person.objects.filter(userId=get_user_id).values('userId', 'userName', 'userType')
    course_info = Course.objects.filter(courseId=get_course_id).values('courseId', 'courseName')
    get_forum_q = ForumQuestion.objects.filter(postId=post_id).values('questionId', 'courseId', 'postId', 'content',
                                                                      'title', 'postTime', 'answerNum')
    return render(request, "administrator_forum_Q_delete.html", locals())

def administrator_forum_A_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_info = Course.objects.all().values('courseId', 'courseName')
    post_id = request.GET.get('postId')
    get_content = request.GET.get('content')
    get_user_id = ForumQuestion.objects.filter(postId=post_id).values_list('questionId', flat=True)[0]
    get_course_id = ForumQuestion.objects.filter(postId=post_id).values_list('courseId', flat=True)[0]
    user_info = Person.objects.filter(userId=get_user_id).values('userId', 'userName', 'userType')
    course_info = Course.objects.filter(courseId=get_course_id).values('courseId', 'courseName')
    get_forum_q = ForumQuestion.objects.filter(postId=post_id).values( 'postId', 'title')
    get_forum_a = ForumAnswer.objects.filter(postId=post_id, content=get_content).values('answerId', 'postId', 'content', 'answerTime')
    return render(request, "administrator_forum_A_delete.html", locals())

def administrator_forum_A_delete_succeed(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    post_id = request.GET.get('postId')
    answer_content = request.GET.get('content')
    get_answer_id = ForumAnswer.objects.filter(content=answer_content, postId=post_id).values_list('answerId', flat=True)[0]
    get_post_id = ForumAnswer.objects.filter(content=answer_content, postId=post_id).values_list('postId', flat=True)[0]
    get_course_id = ForumQuestion.objects.filter(postId=get_post_id).values_list('courseId', flat=True)[0]
    ForumAnswer.objects.filter(content=answer_content, postId=post_id).delete()
    return render(request, "administrator_forum_A_delete_succeed.html", locals())

def administrator_forum_Q_delete_succeed(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    post_id = request.GET.get('postId')
    answer_content = request.GET.get('content')
    get_question_id = ForumQuestion.objects.filter(postId=post_id).values_list('questionId', flat=True)[0]
    get_course_id = ForumQuestion.objects.filter(postId=post_id).values_list('courseId', flat=True)[0]
    ForumQuestion.objects.filter(postId=post_id).delete()
    ForumAnswer.objects.filter(postId=post_id).delete()
    return render(request, "administrator_forum_Q_delete_succeed.html", locals())

def administrator_courselist_stu(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
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
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    student_id = request.GET.get('userId')
    course_id = request.GET.get('courseId')
    student_info = Person.objects.filter(userId=student_id).values('userId', 'userName')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    get_exam_info = Exam.objects.filter(studentId=student_id, courseId=course_id).values('courseId', 'type', 'weight', 'isOver', 'start_time', 'score')
    return render(request, "administrator_student_grades.html", locals())

def administrator_teacherlist(request):    #考试成绩界面
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        keyword = request.GET.get('keyword')
        if keyword is None:
            teacher_info = Person.objects.filter(userType=2).values('userId', 'passWord', 'userName')
            contact_list = teacher_info
        else:
            teacher_info = Person.objects.filter(
                (Q(userType=2)) & (Q(userName__icontains=keyword) | Q(userId__icontains=keyword)))
            contact_list = teacher_info

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
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        keyword = request.POST.get('teacher')
        if keyword is None:
            teacher_id = request.POST.get('id')
            teacher_password = request.POST.get('password')
            teacher_name = request.POST.get('name')
            exist = Person.objects.filter(userId=teacher_id, userType=3).count()
            if exist == 0:
                Person.objects.create(userId=teacher_id, userType=2, userName=teacher_name, passWord=teacher_password)
            teacher_info = Person.objects.filter(userType=2)
            contact_list = teacher_info
        else:
            teacher_info = Person.objects.filter(
                (Q(userType=2)) & (Q(userName__icontains=keyword) | Q(userId__icontains=keyword)))
            contact_list = teacher_info

        contact_list = teacher_info
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

def administrator_teacher_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    teacher_id = request.GET.get('userId')
    teacher_info = Person.objects.filter(userType=2)
    exist = Course.objects.filter(teacherId=teacher_id).count()
    if exist == 0:
        Person.objects.filter(userId=teacher_id).delete()
    contact_list = teacher_info
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
    return render(request, "administrator_teacherlist.html", locals())

def administrator_teacher_details(request):    #在线考试待考课程列表界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    teacher_id = request.GET.get('userId')
    teacher_info = Person.objects.filter(userId=teacher_id)
    return render(request, "administrator_teacher_details.html", locals())

def administrator_courselist_tea(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    teacher_id = request.GET.get('userId')
    teacher_info = Person.objects.filter(userId=teacher_id)
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
    return render(request, "administrator_courselist_tea.html", locals())

def administrator_course_student(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    teacher_id = request.GET.get('userId')
    course_id = request.GET.get('courseId')
    teacher_info = Person.objects.filter(userId=teacher_id).values('userId', 'userName')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'isOver')
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
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    student_id = request.GET.get('userId')
    course_id = request.GET.get('courseId')
    student_info = Person.objects.filter(userId=student_id).values('userId', 'userName')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName', 'teacherId')
    get_exam_info = Exam.objects.filter(studentId=student_id, courseId=course_id).values('courseId', 'type', 'weight', 'isOver', 'start_time', 'score')
    return render(request, "administrator_student_grades_tea.html", locals())

def administrator_init_password(request):    #考试成绩界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    user_id = request.GET.get('userId')
    Person.objects.filter(userId=user_id).update(passWord=123456)
    return render(request, "administrator_init_password.html", locals())

def administrator_question_added(request):    #考试成绩界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    return render(request, "administrator_question_added.html", locals())

def administrator_test_manage(request):    #在线考试待考课程列表界面
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        keyword = request.GET.get('keyword')
        teacher_info = Person.objects.filter(userType=2).values('userId', 'userName')
        if keyword is None:
            course_info = Course.objects.all().values('courseId', 'courseName', 'teacherId', 'isOver')
            contact_list = course_info
        else:
            course_info = Course.objects.filter(Q(courseName__icontains=keyword) | Q(courseId__icontains=keyword))
            contact_list = course_info
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
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        keyword = request.POST.get('course')
        course_info = Course.objects.filter(Q(courseName__icontains=keyword) | Q(courseId__icontains=keyword))
        teacher_info = Person.objects.filter(userType=2).values('userId', 'userName')

        contact_list = course_info
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
    return render(request, "administrator_test_manage.html", locals())

def administrator_course_list(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_info = Course.objects.all()
    get_Q_F = FillInTheBlank.objects.all()
    get_Q_C = ChoiceQuestion.objects.all()

    return render(request, "administrator_course_list.html", locals())

def administrator_question_list(request):    #在线考试待考课程列表界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    return render(request, "administrator_question_list.html", locals())

def administrator_choice_list(request):    #在线考试待考课程列表界面
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
        keyword = request.GET.get('keyword')
        if keyword is None:
            get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id)
            contact_list = get_Q_C
        else:
            get_Q_C = ChoiceQuestion.objects.filter(Q(courseId_id=course_id) & (Q(content__icontains=keyword) | Q(choiceId__icontains=keyword) |
                                                    Q(questionA__contains=keyword) | Q(questionB__contains=keyword) |
                                                    Q(questionC__contains=keyword) | Q(questionD__contains=keyword)))
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
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
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

            exist = ChoiceQuestion.objects.filter(content=get_content, type=get_type, questionA=a, questionB=b, questionC=c,
                                                  questionD=d, answer=answer, courseId_id=course_id).count()
            if exist == 0:
                ChoiceQuestion.objects.create(content=get_content, questionA=a, questionB=b, questionC=c, questionD=d,
                                              answer=answer, type=get_type, courseId_id=course_id)

            course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
            get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id)
            contact_list = get_Q_C
        else:
            get_Q_C = ChoiceQuestion.objects.filter(Q(courseId_id=course_id) & (Q(content__icontains=keyword) | Q(choiceId__icontains=keyword) |
                                                    Q(questionA__contains=keyword) | Q(questionB__contains=keyword) |
                                                    Q(questionC__contains=keyword) | Q(questionD__contains=keyword)))
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
    return render(request, "administrator_choice_list.html", locals())

def administrator_fill_list(request):    #在线考试待考课程列表界面
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        course_id = request.GET.get('courseId')
        course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
        keyword = request.GET.get('keyword')
        if keyword is None:
            get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
            contact_list = get_Q_F

        else:
            get_Q_F = FillInTheBlank.objects.filter(Q(courseId_id=course_id) & (Q(content__icontains=keyword) | Q(fillId__icontains=keyword) |
                                                    Q(answer__icontains=keyword)))
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
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
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
            get_Q_F = FillInTheBlank.objects.filter(Q(courseId_id=course_id) & (Q(content__icontains=keyword) | Q(fillId__icontains=keyword) |
                                                    Q(answer__icontains=keyword)))
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
    return render(request, "administrator_fill_list.html", locals())

def administrator_C_edit(request):
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        question_id = request.GET.get('choiceId')
        page = request.GET.get('page')
        get_question_info = ChoiceQuestion.objects.filter(choiceId=question_id).values('choiceId', 'courseId',
                                                                                       'content',
                                                                                       'answer', 'questionA',
                                                                                       'questionB',
                                                                                       'questionC', 'questionD', 'type')
        course_info = Course.objects.all()
        find_question = TestQuestion.objects.filter(questionId=question_id, type=1).count()
        if find_question is not 0:
            exist = 1
        else:
            exist = 0
        return render(request, "administrator_C_edit.html", locals())
    elif request.method == "POST":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        question_id = request.GET.get('choiceId')
        get_question_info = ChoiceQuestion.objects.filter(choiceId=question_id).values('choiceId')
        page = request.GET.get('page')
        get_content = request.POST.get('content')
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
        return render(request, "administrator_C_edit.html", locals())

def administrator_F_edit(request):
    if request.method == "GET":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        question_id = request.GET.get('fillId')
        course_id = request.GET.get('courseId')
        page = request.GET.get('page')
        get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId', 'courseId', 'content',
                                                                                     'answer', 'type')
        course_info = Course.objects.all()
        find_question = TestQuestion.objects.filter(questionId=question_id, type=2).count()
        if find_question is not 0:
            exist = 1
        else:
            exist = 0
        return render(request, "administrator_F_edit.html", locals())
    elif request.method == "POST":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
        question_id = request.GET.get('fillId')
        get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId')
        page = request.GET.get('page')
        get_content = request.POST.get('content')
        answer = request.POST.get('answer')
        get_type = request.POST.get('type')
        course_id = request.POST.get('courseId')
        FillInTheBlank.objects.filter(fillId=question_id).update(content=get_content, answer=answer, type=get_type,
                                                                 courseId_id=course_id)
        get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId', 'courseId', 'content',
                                                                                     'answer', 'type')
        course_info = Course.objects.all()
        find_question = ExamQuestion.objects.filter(questionId=question_id, type=2).count()
        if find_question is not 0:
            exist = 1
        else:
            exist = 0
        return render(request, "administrator_F_edit.html", locals())

def administrator_C_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    page = request.GET.get('page')
    question_id = request.GET.get('choiceId')
    get_question_info = ChoiceQuestion.objects.filter(choiceId=question_id).values('choiceId', 'courseId', 'content', 'answer', 'questionA', 'questionB', 'questionC', 'questionD', 'type')
    course_info = Course.objects.all()
    find_question = TestQuestion.objects.filter(questionId=question_id, type=1).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "administrator_C_delete.html", locals())

def administrator_F_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    page = request.GET.get('page')
    course_id = request.GET.get('courseId')
    question_id = request.GET.get('fillId')
    get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId', 'courseId', 'content', 'answer', 'type')
    course_info = Course.objects.all()
    find_question = TestQuestion.objects.filter(questionId=question_id, type=2).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "administrator_F_delete.html", locals())

def administrator_F_delete_succeed(request):
    question_id = request.GET.get('questionId')
    course_id = FillInTheBlank.objects.filter(fillId=question_id).values_list('courseId', flat=True)[0]
    FillInTheBlank.objects.filter(fillId=question_id).delete()
    page = request.GET.get('page')
    return render(request, "administrator_F_delete_succeed.html", locals())

def administrator_C_delete_succeed(request):
    question_id = request.GET.get('questionId')
    course_id = ChoiceQuestion.objects.filter(choiceId=question_id).values_list('courseId', flat=True)[0]
    ChoiceQuestion.objects.filter(choiceId=question_id).delete()
    page = request.GET.get('page')
    return render(request, "administrator_C_delete_succeed.html", locals())

def administrator_failed_page(request):
    return render(request, "administrator_failed_page.html", locals())

def administrator_feedback(request):    #在线考试待考课程列表界面
    return render(request, "administrator_feedback.html")

def administrator_exam_Q(request):    #已通过成绩页面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    get_type = request.GET.get('type')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    student_info = Person.objects.filter(userType=3).values('userId', 'userName')
    get_student_id = CourseStudent.objects.filter(courseId=course_id).values('studentId')
    get_exam_score = Exam.objects.filter(courseId=course_id, type=get_type).values('studentId', 'courseId', 'type', 'weight', 'isOver', 'score')

    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA', 'questionB', 'questionC', 'questionD', 'type')

    get_test_id = Test.objects.filter(courseId=course_id, type=get_type).values_list('testId', flat=True)[0]
    print(get_test_id)
    get_Q_id = TestQuestion.objects.filter(testId=get_test_id).values('questionId', 'type')
    test_info = Test.objects.filter(testId=get_test_id).values('courseId', 'type', 'weight','isReady')
    return render(request, "administrator_exam_Q.html", locals())

def administrator_exam_grade(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    get_type = request.GET.get('type')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    student_info = Person.objects.filter(userType=3).values('userId', 'userName')
    get_student_id = CourseStudent.objects.filter(courseId=course_id).values('studentId')
    test_info = Test.objects.filter(courseId=course_id, type=get_type).values('isReady', 'type')
    get_exam_score = Exam.objects.filter(courseId=course_id, type=get_type).values('studentId', 'courseId', 'type', 'weight', 'isOver', 'score')

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
    return render(request, "administrator_exam_grade.html", locals())




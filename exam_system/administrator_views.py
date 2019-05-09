from django.shortcuts import render
from.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

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
            return render(request, 'administrator_error_stu.html')

def administrator_studentlist(request):    #考试成绩界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    student_info = Person.objects.filter(userType=3).values('userId', 'passWord').distinct()
    user_info = Person.objects.all().values('userId', 'passWord', 'userName')

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
    print(get_answer_id)
    print(get_post_id)
    print(get_course_id)
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
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
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

def administrator_member_added(request):    #考试成绩界面
    return render(request, "administrator_member_added.html", locals())

def administrator_question_added(request):    #考试成绩界面
    return render(request, "administrator_question_added.html", locals())

def administrator_test_manage(request):    #在线考试待考课程列表界面
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_info = Course.objects.all().values('courseId', 'courseName', 'teacherId', 'isOver')
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

    get_Q_F = FillInTheBlank.objects.filter(courseId=course_id).values('fillId', 'content', 'answer', 'type')
    get_Q_C = ChoiceQuestion.objects.filter(courseId=course_id).values('choiceId', 'content', 'answer', 'questionA', 'questionB', 'questionC', 'questionD', 'type')

    contact_list1 = get_Q_F
    contact_list2 = get_Q_C

    paginator = Paginator(contact_list1, 5)  # 每页5条
    paginator = Paginator(contact_list2, 5)

    page = request.GET.get('page')
    try:
        contacts1 = paginator.page(page)  # contacts为Page对象！
        contacts2 = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts1 = paginator.page(1)
        contacts2 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts1 = paginator.page(paginator.num_pages)
        contacts2 = paginator.page(paginator.num_pages)
    return render(request, "administrator_question_list.html", locals())

def administrator_C_edit(request):
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
    find_question = ExamQuestion.objects.filter(questionId=question_id, type=1).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "administrator_C_edit.html", locals())

def administrator_F_edit(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
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
    return render(request, "administrator_F_edit.html", locals())

def administrator_C_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    page = request.GET.get('page')
    question_id = request.GET.get('choiceId')
    get_question_info = ChoiceQuestion.objects.filter(choiceId=question_id).values('choiceId', 'courseId', 'content', 'answer', 'questionA', 'questionB', 'questionC', 'questionD', 'type')
    course_info = Course.objects.all()
    find_question = ExamQuestion.objects.filter(questionId=question_id, type=1).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "administrator_C_delete.html", locals())

def administrator_F_delete(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    page = request.GET.get('page')
    question_id = request.GET.get('fillId')
    get_question_info = FillInTheBlank.objects.filter(fillId=question_id).values('fillId', 'courseId', 'content', 'answer', 'type')
    course_info = Course.objects.all()
    find_question = ExamQuestion.objects.filter(questionId=question_id, type=2).count()
    if find_question is not 0:
        exist = 1
    else:
        exist = 0
    return render(request, "administrator_F_delete.html", locals())

def administrator_C_delete_succeed(request):
    question_id = request.GET.get('questionId')
    ChoiceQuestion.objects.filter(choiceId=question_id).delete()
    page = request.GET.get('page')
    return render(request, "administrator_C_delete_succeed.html", locals())

def administrator_F_delete_succeed(request):
    question_id = request.GET.get('questionId')
    FillInTheBlank.objects.filter(fillId=question_id).delete()
    page = request.GET.get('page')
    return render(request, "administrator_F_delete_succeed.html", locals())

def administrator_F_edit_succeed(request):
    if request.method == "GET":
        return render(request, "administrator_F_edit_succeed.html", locals())
    elif request.method == "POST":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
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
    return render(request, "administrator_F_edit_succeed.html", locals())

def administrator_C_edit_succeed(request):
    if request.method == "GET":
        return render(request, "administrator_C_edit_succeed.html", locals())
    elif request.method == "POST":
        administrator_id = request.session.get('administrator_id')
        administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
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
        return render(request, "administrator_C_edit_succeed.html", locals())

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

    get_first_exam_id = Exam.objects.filter(courseId=course_id, type=get_type).values_list('examId', flat=True).first()
    get_frst_Q_id = ExamQuestion.objects.filter(examId=get_first_exam_id).values('questionId', 'type')
    return render(request, "administrator_exam_Q.html", locals())

def administrator_exam_grade(request):
    administrator_id = request.session.get('administrator_id')
    administrator_name = Person.objects.filter(userId=administrator_id).values('userId', 'userName')
    course_id = request.GET.get('courseId')
    get_type = request.GET.get('type')
    course_info = Course.objects.filter(courseId=course_id).values('courseId', 'courseName')
    student_info = Person.objects.filter(userType=3).values('userId', 'userName')
    get_student_id = CourseStudent.objects.filter(courseId=course_id).values('studentId')
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

def test(request):    #未通过成绩界面
    return render(request, "测试.html", locals())



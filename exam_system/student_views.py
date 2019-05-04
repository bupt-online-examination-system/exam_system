from django.shortcuts import render
from.models import *
from django.contrib.auth.decorators import login_required
from graduation_project import settings
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.aggregates import Min
from django.contrib.auth import authenticate
import MySQLdb

def student_login(request): #学生界面模板
    return render(request, "student_login.html",locals())

def exam_list(request):    #在线考试待考课程列表界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    exam_course_info = Exam.objects.filter(~Q(type=5),studentId=studentId,isOver=1).values('courseId').distinct()
    print(exam_course_info)
    course_info = Course.objects.all().values('courseId','courseName')
    return render(request, "exam_list.html",locals())

def mistake_list(request):    #错题集课程列表界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    my_course_info = CourseStudent.objects.filter(studentId=studentId).values('courseId')
    course_info = Course.objects.all().values('courseId','courseName')
    return render(request, "mistake_list.html",locals())

def mistake_choice(request):    #该课程错题集选择题练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")
    print(courseId)

    deleteMistake = request.GET.get("deleteMistake")  #判断是否点击了从错题集中删除此题按钮
    print(deleteMistake)
    choiceId = request.GET.get("choiceId")
    print(choiceId)
    if deleteMistake is not None and choiceId is not None:
        MistakesCollection.objects.filter(type=1,questionId=choiceId).delete()

    exam_question_info = MistakesCollection.objects.filter(studentId=studentId,type=1,courseId=courseId).values('questionId')#该课程选择题所有练习题号
    print(exam_question_info)
    choice_question_info = ChoiceQuestion.objects.filter(type=2)#所有选择题练习信息
    print(choice_question_info)

    contact_list = exam_question_info
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
    return render(request, "mistake_choice.html", locals())

def mistake_fill(request):    #该课程错题集填空题练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")

    deleteMistake = request.GET.get("deleteMistake")  #判断是否点击了从错题集中删除此题按钮
    print(deleteMistake)
    fillId = request.GET.get("fillId")
    print(fillId)
    if deleteMistake is not None and fillId is not None:
        MistakesCollection.objects.filter(type=2,questionId=fillId).delete()

    exam_question_info = MistakesCollection.objects.filter(studentId=studentId,type=2,courseId=courseId).values('questionId')#该课程填空题所有练习题号
    print(exam_question_info)
    fill_question_info = FillInTheBlank.objects.filter(type=2)#所有填空题练习信息
    print(fill_question_info)

    contact_list = exam_question_info
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
    return render(request, "mistake_fill.html", locals())

def mistake_choice_details(request):    #该课程错题集选择题详情练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    choiceId = request.GET.get("choiceId")
    print(choiceId)
    choice_question_info = ChoiceQuestion.objects.filter(choiceId=choiceId)#所有选择题练习信息
    print(choice_question_info)
    return render(request, "mistake_choice_details.html", locals())

def mistake_choice_details_answer(request):    #该课程错题集选择题详情练习界面(有答案)
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    choiceId = request.GET.get("choiceId")
    print(choiceId)
    choice_question_info = ChoiceQuestion.objects.filter(choiceId=choiceId)#所有选择题练习信息
    print(choice_question_info)
    return render(request, "mistake_choice_details_answer.html", locals())

def mistake_fill_details(request):    #该课程错题集填空题详情练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    fillId = request.GET.get("fillId")
    print(fillId)
    fill_question_info = FillInTheBlank.objects.filter(fillId=fillId)#所有填空题练习信息
    print(fill_question_info)
    return render(request, "mistake_fill_details.html", locals())

def mistake_fill_details_answer(request):    #该课程错题集填空题详情练习界面(有答案)
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    fillId = request.GET.get("fillId")
    print(fillId)
    fill_question_info = FillInTheBlank.objects.filter(fillId=fillId)#所有填空题练习信息
    print(fill_question_info)
    return render(request, "mistake_fill_details_answer.html", locals())

def practice_list(request):    #练习课程列表界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    my_course_info = CourseStudent.objects.filter(studentId=studentId).values('courseId')
    course_info = Course.objects.all().values('courseId','courseName')
    return render(request, "practice_list.html",locals())

def practice_choice(request):    #该课程选择题练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")
    print(courseId)
    examId = list(Exam.objects.filter(studentId=studentId,courseId=courseId,type=5).values_list('examId', flat=True)) #得到该学生该课程练习的examId
    if(examId == []):
        return render(request, "practice_choice.html")
    exam_question_info = ExamQuestion.objects.filter(examId=examId[0],type=1).values('questionId')#该课程选择题所有练习题号
    print(exam_question_info)
    choice_question_info = ChoiceQuestion.objects.filter(type=2)#所有选择题练习信息
    print(choice_question_info)

    contact_list = exam_question_info
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
    return render(request, "practice_choice.html", locals())

def practice_fill(request):    #该课程填空题练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")
    examId = list(Exam.objects.filter(studentId=studentId,courseId=courseId,type=5).values_list('examId', flat=True)) #得到该学生该课程练习的examId
    if(examId == []):
        return render(request, "practice_fill.html")
    exam_question_info = ExamQuestion.objects.filter(examId=examId[0],type=2).values('questionId')#该课程填空题所有练习题号
    print(exam_question_info)
    fill_question_info = FillInTheBlank.objects.filter(type=2)#所有填空题练习信息
    print(fill_question_info)

    contact_list = exam_question_info
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
    return render(request, "practice_fill.html", locals())

def practice_choice_details(request):    #该课程选择题详情练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    choiceId = request.GET.get("choiceId")
    print(choiceId)

    addMistake = request.GET.get("addMistake")  #判断是否点击了添加到错题集按钮
    print(addMistake)
    courseId = list(ChoiceQuestion.objects.filter(choiceId=choiceId).values_list('courseId',flat=True))
    if addMistake is not None:
        studentIdInstance = Person.objects.get(userId=studentId)
        courseIdInstance = Course.objects.get(courseId=courseId[0])
        MistakesCollection.objects.create(studentId=studentIdInstance,courseId=courseIdInstance,questionId=choiceId,type=1)

    choice_question_info = ChoiceQuestion.objects.filter(choiceId=choiceId)#所有选择题练习信息
    print(choice_question_info)
    mistake_info = MistakesCollection.objects.filter(questionId=choiceId,type=1)#错题集中寻找
    print(mistake_info)
    return render(request, "practice_choice_details.html", locals())

def practice_choice_details_answer(request):    #该课程选择题详情练习界面(有答案)
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    choiceId = request.GET.get("choiceId")
    print(choiceId)

    addMistake = request.GET.get("addMistake")  #判断是否点击了添加到错题集按钮
    print(addMistake)
    courseId = list(ChoiceQuestion.objects.filter(choiceId=choiceId).values_list('courseId',flat=True))
    if addMistake is not None:
        studentIdInstance = Person.objects.get(userId=studentId)
        courseIdInstance = Course.objects.get(courseId=courseId[0])
        MistakesCollection.objects.create(studentId=studentIdInstance,courseId=courseIdInstance,questionId=choiceId,type=1)

    choice_question_info = ChoiceQuestion.objects.filter(choiceId=choiceId)#所有选择题练习信息
    print(choice_question_info)
    mistake_info = MistakesCollection.objects.filter(questionId=choiceId,type=1)#错题集中寻找
    return render(request, "practice_choice_details_answer.html", locals())

def practice_fill_details(request):    #该课程填空题详情练习界面
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    fillId = request.GET.get("fillId")
    print(fillId)

    addMistake = request.GET.get("addMistake")  #判断是否点击了添加到错题集按钮
    print(addMistake)
    courseId = list(FillInTheBlank.objects.filter(fillId=fillId).values_list('courseId',flat=True))
    if addMistake is not None:
        studentIdInstance = Person.objects.get(userId=studentId)
        courseIdInstance = Course.objects.get(courseId=courseId[0])
        MistakesCollection.objects.create(studentId=studentIdInstance,courseId=courseIdInstance,questionId=fillId,type=2)

    fill_question_info = FillInTheBlank.objects.filter(fillId=fillId)#所有填空题练习信息
    print(fill_question_info)
    mistake_info = MistakesCollection.objects.filter(questionId=fillId,type=2)#错题集中寻找
    return render(request, "practice_fill_details.html", locals())

def practice_fill_details_answer(request):    #该课程填空题详情练习界面(有答案)
    studentId = request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    fillId = request.GET.get("fillId")
    print(fillId)

    addMistake = request.GET.get("addMistake")  #判断是否点击了添加到错题集按钮
    print(addMistake)
    courseId = list(FillInTheBlank.objects.filter(fillId=fillId).values_list('courseId',flat=True))
    if addMistake is not None:
        studentIdInstance = Person.objects.get(userId=studentId)
        courseIdInstance = Course.objects.get(courseId=courseId[0])
        MistakesCollection.objects.create(studentId=studentIdInstance,courseId=courseIdInstance,questionId=fillId,type=2)

    fill_question_info = FillInTheBlank.objects.filter(fillId=fillId)#所有填空题练习信息
    print(fill_question_info)
    mistake_info = MistakesCollection.objects.filter(questionId=fillId,type=2)#错题集中寻找
    return render(request, "practice_fill_details_answer.html", locals())

def exam_details(request):    #考试详情界面
    if request.method == "GET":
        studentId = request.session.get('studentId')
        studentName = Person.objects.filter(userId=studentId).values('userName')
        courseId = request.GET.get("courseId")
        examId = list(Exam.objects.filter(studentId=studentId,courseId=courseId,isOver=1).values_list('examId',flat=True).order_by('examId')) #得到该学生该课程下一次考试的examId
        if(examId == []):
            return render(request, "exam_details.html")
        exam_question_info = ExamQuestion.objects.filter(examId=examId[0]).values('questionId','type')
        choice_question_info = ChoiceQuestion.objects.filter(type=1)
        fill_question_info = FillInTheBlank.objects.filter(type=1)

        contact_list = exam_question_info
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
        return render(request, "exam_details.html", locals())
    elif request.method == "POST":
        a = request.POST.get('choice')
        print(a)
        # b = request.POST.get('choice2')
        # print(b)
        # c = request.POST.get('choice3')
        # print(c)
        # d = request.POST.get('choice4')
        # print(d)
    return render(request, "exam_details.html", locals())

def personal_homepage(request):    #在个人主页界面
    if request.method == "GET":
        return render(request, "personal_homepage.html", locals())
    elif   request.method == "POST":
        studentId = request.POST.get('userId')
        student_password = request.POST.get("passWord")
        login_user_type = list(Person.objects.filter(userId=studentId).values_list('userType',flat=True))
        studentName = Person.objects.filter(userId=studentId).values('userName')
        count = Person.objects.filter(userId=studentId).count()
        if count == 1 and login_user_type[0] == 3:
            real_password = list(Person.objects.filter(userId=studentId).values_list('passWord',flat=True))
            if student_password == real_password[0]:
                request.session['studentId'] = studentId
                return render(request, "personal_homepage.html", locals())
            else:
                return render(request, 'administrator_error_stu.html')
        else:
            return render(request, 'administrator_error_stu.html')

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
    exam_details_info = Exam.objects.filter(~Q(type=5),courseId=courseId).values('type','score')
    return render(request, "pass_exam_details.html", locals())

def fail_exam_details(request):    #未通过课程考试信息详情界面
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    courseId = request.GET.get("courseId")
    exam_details_info = Exam.objects.filter(~Q(type=5),courseId=courseId).values('type','score')
    return render(request, "fail_exam_details.html", locals())

def exam_schedule(request):    #待考课程界面
    studentId=request.session.get('studentId')
    studentName = Person.objects.filter(userId=studentId).values('userName')
    over_course = list(Exam.objects.filter(isOver=2,type=4).values_list('courseId', flat=True))#所有期末考结束的课
    print(over_course)
    length = len(over_course)
    for i in range(length):
        Course.objects.filter(courseId=over_course[i]).update(isOver=2)   #把期末考结课的课程状态改为已结课
    exam_schedule_info = Course.objects.filter(isOver=1).values('courseId','courseName') #找出所有期末考未结束的课
    my_exam_schedule_info = CourseStudent.objects.filter(studentId=studentId).values('courseId')#当前登录学生所选的课程
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
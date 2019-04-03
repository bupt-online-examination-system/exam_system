from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 用户信息模板

class Person(models.Model):
    userId = models.AutoField(primary_key=True)  # 用户id
    userType = models.IntegerField()            # 用户类型(1:管理员  2：老师  3：学生)
    userName = models.CharField(max_length=50)  # 用户姓名
    passWord = models.CharField(max_length=50)  # 用户密码


# 课程信息模板
class Course(models.Model):
    courseId = models.AutoField(primary_key=True)                                                     # 课程id
    teacherId = models.ForeignKey('Person', related_name='teacher_course', on_delete=models.CASCADE)  # 教师id
    courseName = models.CharField(max_length=50)  # 课程名称
    isOver = models.IntegerField(default=1)  # 该课程是否结束，即最后一次考试已结束(1:未结课  2：已结课)


# 学生-课程对照关系
class CourseStudent(models.Model):
    courseId = models.ForeignKey('Course', related_name='course_student', on_delete=models.CASCADE)  # 课程id
    studentId = models.ForeignKey('Person', related_name='student_course', on_delete=models.CASCADE)  # 学生id


# 考试信息模板
class Exam(models.Model):
    examId = models.AutoField(primary_key=True)  # 考试试卷id
    courseId = models.ForeignKey('Course', related_name='course_exam', on_delete=models.CASCADE)  # 课程id
    studentId = models.ForeignKey('Person', related_name='Person_exam', on_delete=models.CASCADE)  # 学生id
    isOver = models.IntegerField(default=1)  # 考试是否结束(1:未结束  2：已结束)
    score = models.IntegerField(default=-1)  # 考试分数
    type = models.IntegerField()  # 考试类型(1：第一次月考  2：期中考 3：第二次月考 4：期末考 5：练习)


# 试卷-题目对照关系
class ExamQuestion(models.Model):
    examId = models.ForeignKey('Exam', related_name='exam_question', on_delete=models.CASCADE)  # 考试试卷id
    questionId = models.IntegerField()  # 题目id
    answer = models.CharField(max_length=50, blank=True, null=True)  # 学生给出的答案
    type = models.IntegerField()  # 题目类型(1：选择  2：填空)


# 选择题信息模板
class ChoiceQuestion(models.Model):
    choiceId = models.AutoField(primary_key=True)  # 选择题id
    courseId = models.CharField(max_length=50)  # 课程id
    content = models.CharField(max_length=50)  # 题目内容
    questionA = models.CharField(max_length=50)  # 选项A
    questionB = models.CharField(max_length=50)  # 选项B
    questionC = models.CharField(max_length=50)  # 选项C
    questionD = models.CharField(max_length=50)  # 选项D
    answer = models.CharField(max_length=50)  # 正确答案
    type = models.IntegerField()  # 题目类型(1：考试  2：练习)


# 填空题信息模板
class FillInTheBlank(models.Model):
    fillId = models.AutoField(primary_key=True)  # 填空题id
    courseId = models.CharField(max_length=50)  # 课程id
    content = models.CharField(max_length=50)  # 题目内容
    answer = models.CharField(max_length=50)  # 正确答案
    type = models.IntegerField()  # 题目类型(1：考试  2：练习)


# 学生成绩模板
class Grade(models.Model):
    studentId = models.ForeignKey('Person', related_name='Person_grade', on_delete=models.CASCADE)  # 学生id
    courseId = models.ForeignKey('Course', related_name='course_grade', on_delete=models.CASCADE)  # 课程id
    grade = models.IntegerField()  # 学生该门课程最终成绩(多次考试加权得出，注意结果是整数可能要四舍五入)
    isPass = models.IntegerField()  # 是否通过考试(1：及格  2：不及格)


# 错题集信息模板
class MistakesCollection(models.Model):
    studentId = models.ForeignKey('Person', related_name='Person_mistake', on_delete=models.CASCADE)  # 学生id
    courseId = models.ForeignKey('Course', related_name='course_mistake', on_delete=models.CASCADE)  # 课程id
    choiceId = models.ForeignKey('ChoiceQuestion', on_delete=models.CASCADE)  # 选择题id
    fillId = models.ForeignKey('FillInTheBlank', on_delete=models.CASCADE)  # 填空题id


# 论坛发帖信息模板
class ForumQuestion(models.Model):
    postId = models.AutoField(primary_key=True)  # 帖子id
    questionId = models.ForeignKey('Person', related_name='forum_question', on_delete=models.CASCADE)  # 发帖人id
    content = models.CharField(max_length=50)  # 帖子的内容
    title = models.CharField(max_length=50)  # 帖子的标题
    courseId = models.ForeignKey('Course', related_name='course_forum_question', on_delete=models.CASCADE)  # 课程id
    postTime = models.DateTimeField(default='1970-01-01 00:00:00')  # 发帖时间
    topTime = models.DateTimeField(default='1970-01-01 00:00:00')  # 上一次置顶时间


# 论坛回帖信息模板
class ForumAnswer(models.Model):
    postId = models.ForeignKey('ForumQuestion', related_name='forum_question', on_delete=models.CASCADE)  # 帖子id
    answerId = models.ForeignKey('Person', related_name='forum_answer', on_delete=models.CASCADE)  # 回帖人id
    content = models.CharField(max_length=50)  # 回复的内容
    answerTime = models.DateTimeField(default='1970-01-01 00:00:00')  # 回复时间


# 考试历史信息模板
class History(models.Model):
    studentId = models.ForeignKey('Person', related_name='Person_history', on_delete=models.CASCADE)  # 学生id
    courseId = models.ForeignKey('Course', related_name='course_history', on_delete=models.CASCADE)  # 课程id
    examId = models.ForeignKey('Exam', related_name='exam_history', on_delete=models.CASCADE)  # 考试试卷id
    ip = models.CharField(max_length=50)  # ip
    time = models.DateTimeField(default='1970-01-01 00:00:00')  # 考试登录时的时间



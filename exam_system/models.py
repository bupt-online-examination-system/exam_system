# from django.db import models
# #问题1：课程不能删除，否则要设置级联删除
# #问题2：已经组卷的题目不能删除吧？这样设置级联删除也没意义了，删题目加个逻辑判断是否已经被用于出卷？
#
# # Create your models here.
# # 用户信息模板
# class User(models.Model):
#     userId = models.CharField(max_length=50, primary_key=True)  #用户id
#     userType = models.IntegerField()                            #用户类型(1:管理员  2：老师  3：学生)
#     userName = models.CharField(max_length=50)                  #用户姓名
#     passWord = models.CharField(max_length=50)                  #用户密码
#
# # 课程信息模板
# class Course(models.Model):
#     courseId = models.CharField(max_length=50)                        #课程id
#     teacherId = models.ForeignKey('User', on_delete=models.CASCADE)   #教师id
#     studentId = models.ForeignKey('User', on_delete=models.CASCADE)   #学生id
#     courseName = models.CharField(max_length=50)                      #课程名称
#     isOver = models.IntegerField()                                    #该课程是否结束，即教师已经打完分(1:未结课  2：已结课)
#
#
# # 考试信息模板
# class Exam(models.Model):
#     examId = models.IntegerField()                                            #考试试卷id
#     courseId = models.CharField(max_length=50)                                #课程id
#     studentId = models.ForeignKey('User', on_delete=models.CASCADE)           #学生id
#     choiceId = models.ForeignKey('ChoiceQuestion', on_delete=models.CASCADE)  #选择题id
#     fillId = models.ForeignKey('FillInTheBlank', on_delete=models.CASCADE)    #填空题id
#     isOver = models.IntegerField()                                            #考试是否结束(1:未结束  2：已结束)
#     score = models.IntegerField()                                             #考试分数
#     type = models.IntegerField()                                              #考试类型(1：考试  2：练习)
#
#
# # 选择题信息模板
# class ChoiceQuestion(models.Model):
#     choiceId = models.CharField(max_length=50, primary_key=True)  #选择题id
#     courseId = models.CharField(max_length=50)                    #课程id
#     content = models.CharField(max_length=50)                     #题目内容
#     questionA = models.CharField(max_length=50)                   #选项A
#     questionB = models.CharField(max_length=50)                   #选项B
#     questionC = models.CharField(max_length=50)                   #选项C
#     questionD = models.CharField(max_length=50)                   #选项D
#     answer = models.CharField(max_length=50)                      #答案
#     type = models.IntegerField()                                  #题目类型(1：考试  2：练习)
#
#
# # 填空题信息模板
# class FillInTheBlank(models.Model):
#     fillId = models.CharField(max_length=50, primary_key=True)   #填空题id
#     courseId = models.CharField(max_length=50)                   #课程id
#     content = models.CharField(max_length=50)                    #题目内容
#     answer = models.CharField(max_length=50)                     #答案
#     type = models.IntegerField()                                 #题目类型(1：考试  2：练习)
#
# # 学生成绩模板
# class Grade(models.Model):
#     studentId = models.ForeignKey('User', on_delete=models.CASCADE) #学生id
#     courseId =models.CharField(max_length=50)                       #课程id
#     grade = models.IntegerField()                                   #学生该门课程最终成绩(多次考试加权得出)
#     isPass = models.IntegerField()                                  #是否通过考试(1：及格  2：不及格)
#
# # 错题集信息模板
# class MistakesCollection(models.Model):
#     studentId = models.ForeignKey('User', on_delete=models.CASCADE)           #学生id
#     courseId =models.CharField(max_length=50)                                 #课程id
#     choiceId = models.ForeignKey('ChoiceQuestion', on_delete=models.CASCADE)  #选择题id
#     fillId = models.ForeignKey('FillInTheBlank', on_delete=models.CASCADE)    #填空题id
#
# # 论坛信息模板
# class Forum(models.Model):
#     questionId = models.ForeignKey('User', on_delete=models.CASCADE)       #发帖人id
#     answerId = models.ForeignKey('User', on_delete=models.CASCADE)         #回帖人id
#     content = models.CharField(max_length=50)                              #帖子(回复)的内容
#     title = models.CharField(max_length=50)                                #帖子的标题
#     courseId =models.CharField(max_length=50)                              #课程id
#
# #考试历史信息模板
# class History(models.Model):
#     studentId = models.ForeignKey('User', on_delete=models.CASCADE)           #学生id
#     courseId =models.CharField(max_length=50)                                 #课程id
#     examId = models.IntegerField()                                            #考试试卷id
#     ip = models.CharField(max_length=50)                                      #ip
#     time = models.DateTimeField()                                             #考试登录时的时间
#
#

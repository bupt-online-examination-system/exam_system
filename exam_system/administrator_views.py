from django.shortcuts import render
from django.http import HttpResponse
from graduation_project import settings
from django.contrib.auth.decorators import login_required
import MySQLdb
import re
import random
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from django.views.generic.base import View


def index(request): #管理员界面模板
    return render(request, "index.html")

def administrator_login(request): #管理员界面模板
    return render(request, "administrator_login.html")

def administrator_mlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_mlist.html")

def administrator_tlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_tlist.html")

def administrator_qlist(request):    #在线考试待考课程列表界面
    return render(request, "administrator_qlist.html")

def administrator_fmanage(request):    #在线考试待考课程列表界面
    return render(request, "administrator_fmanage.html")

def administrator_feedback(request):    #在线考试待考课程列表界面
    return render(request, "administrator_feedback.html")

def administrator_studentlist(request):    #考试成绩界面
    return render(request, "administrator_studentlist.html",locals())

def administrator_teacherlist(request):    #考试成绩界面
    return render(request, "administrator_teacherlist.html",locals())

def administrator_aftlist(request):    #已通过成绩页面
    return render(request, "administrator_aftlist.html", locals())

def administrator_uftlist(request):    #未通过成绩界面
    return render(request, "administrator_uftlist.html", locals())


class login():
    def LOGIN(request):
        # 判断是否为 post请求
        if request.POST:
            # 取输入信息
            userid= request.POST['userId']
            password = request.POST['passWord']

            # # 检测是否有sql注入
            # check_result = login.checkSql(userId, passWord)
            # if check_result == 'wrring':
            #     return HttpResponse('想注入我没那么简单！')

                # 验证用户名
            real_passwd = login.getPasswd(userid)

            if real_passwd == "ERROR":
                return HttpResponse('没有这个用户名!')

            print(real_passwd, password)

            # 验证密码
            if password == real_passwd:
                usertype = login.getUsertype(userid)
                if usertype == 1:
                    # 渲染网页
                    connect = {
                        'login_result': "管理员登录成功!",
                    }
                    return render(request, "administrator_login.html", connect)
                elif usertype == 2:
                    connect = {
                        'login_result': "教师登陆成功"
                    }
                    return render(request, 'teacher_login.html', connect)
                else:
                    connect = {
                        'login_result': "学生登陆成功"
                    }
                    return render(request, 'student_login.html', connect)
            else:
                return HttpResponse("密码错误！")

    def getUsertype(userId):
        # 取用户类型
        conn = MySQLdb.connect(host="localhost",user="root",password="root",db="exam_system",charset="utf8")
        cursor = conn.cursor()
        sql = 'select userType from exam_system_person where userId= "{}"'.format(userId)
        userType = cursor.fetchone()[0]


    def getPasswd(userId):
        # 取正确密码
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="userinformation", charset="utf8")
        cursor = conn.cursor()
        sql = 'select passWord from exam_system_person where userId = "{}"'.format(userId)
        sql_return = cursor.execute(sql)

        # 如果出现错误返回 ERROR
        if sql_return == 0:
            conn.close()
            return "ERROR"
        elif sql_return == 1:
            passWord = cursor.fetchone()
            conn.close()
            return passWord[0]


    # def getUserInfo(userId):
    #     # 取个人信息
    #     print('getting info')
    #     conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="userinformation", charset="utf8")
    #     cursor = conn.cursor()
    #
    #     try:
    #         # 这里代码比较凌乱 因为刚学 django 和 mysql 不长时间 所以不知道有什么好的语法
    #         cursor.execute('select name from userinfo where Uid = "{}"'.format(Uid))
    #         username = cursor.fetchone()[0]
    #         cursor.execute('select sex from userinfo where Uid = "{}"'.format(Uid))
    #         sex = cursor.fetchone()[0]
    #         cursor.execute('select age from userinfo where Uid = "{}"'.format(Uid))
    #         age = cursor.fetchone()[0]
    #         cursor.execute('select Email from userinfo where Uid = "{}"'.format(Uid))
    #         Email = cursor.fetchone()[0]
    #         cursor.execute('select tel from userinfo where Uid = "{}"'.format(Uid))
    #         tel = cursor.fetchone()[0]
    #         conn.close()
    #         print(username, sex, age, Email, tel)
    #
    #         # 返回1 代表成功获取信息
    #         # 后面的list 是个人信息
    #         return 1, [username, sex, age, Email, tel]
    #
    #     except:
    #         conn.close()
    #         return 0, []


    def checkSql(inputUserid, inputPassword):
        #判断是否有sql注入
        if inputUserid[-1] == '\'':
            print('有人尝试注入！')
            return 'wrring'
        elif inputPassword[-1] == '\'':
            print('有人尝试注入！')
            return 'wrring'
        else:
            return 0

    def administrator_login(response):
        # 显示主页
        connect = {}
        return render(response, 'administrator_login.html', connect)

    def teacher_login(response):
        # 显示主页
        connect = {}
        return render(response, 'teacher_login.html', connect)

    def student_login(response):
        # 显示主页
        connect = {}
        return render(response, 'student_login.html', connect)
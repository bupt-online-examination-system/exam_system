from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from graduation_project import settings
from django.http import HttpResponse
def student_login(request):
    return render(request, "student_login.html")
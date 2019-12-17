# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from management.models import Student, Teacher,Lesson,Score
from django.shortcuts import render
from django.http import HttpResponseRedirect
import xlrd
# Create your views here.
def index(request):
    return render(request, "login.html")

def change(request):
        lid = int(request.GET['lid'])
        sid = int(request.GET['sid'])
        sscore = request.POST.get("score", None)
        Score.objects.filter(id=sid).update(score=sscore)
        score = Score.objects.filter(lNum=lid)
        teacher = Teacher.objects.get(t_lesson_id=lid)
        return render(request, "teacher.html", {"teacher": teacher, "score": score})

def add_student(request):
    file_path = "./upload/python名单.xls"
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    student_list_to_insert = list()
    for x in l:
        student_list_to_insert.append(Student(s_number = x[0], s_name=x[1], grade=x[2], subject=x[3], sex=x[4], s_pass=x[5]))
    Student.objects.bulk_create(student_list_to_insert)
    #return render(request, "login.html")

def add_teacher(request):
    file_path = "./upload/teacher.xls"
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    teacher_list_to_insert = list()
    for x in l:
        teacher_list_to_insert.append(Teacher(t_number = x[0], t_name=x[1], t_college=x[2], t_pass=x[3]))
    Teacher.objects.bulk_create(teacher_list_to_insert)
    #return render(request, "login.html")

def add_lesson(request):
    file_path = "./upload/lesson.xls"
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    list_to_insert = list()
    for x in l:
        list_to_insert.append(Lesson(l_number = x[0], l_name=x[1], credit=x[2], l_teacher=Teacher.objects.get(t_name=x[3]), time=x[4]))
    Lesson.objects.bulk_create(list_to_insert)
    #return render(request, "login.html")

def add_xuanke(request):
    file_path = "./upload/xuanke.xls"
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    list_to_insert = list()
    for x in l:
        list_to_insert.append(Score(S_lesson = Lesson.objects.get(l_name = x[0]), S_student = Student.objects.get(s_name = x[1])))
    Score.objects.bulk_create(list_to_insert)
    #return render(request, "login.html")


def testdb(request):
    add_student(request)
    add_teacher(request)
    add_lesson(request)
    add_xuanke(request)
    return render(request, "login.html")

def login(request):
    print (request.POST.get("sid", None))
    if request.method == "POST":
        type = request.POST.get("fruit")
        name = request.POST.get("username", None)
        ps = request.POST.get("password", None)

    print (type)
    if type == "1":
        try:
            s = Student.objects.get(s_number=name)
        except Student.DoesNotExist:
            return HttpResponseRedirect("/")
        if s.s_pass == ps:
            student = Student.objects.get(s_number=name)
            score = Score.objects.filter(S_student=s)
            return render(request, "student.html", {"student": student, "score": score})
        else:
            return HttpResponseRedirect("/")
    elif type == "2":
        try:
            t = Teacher.objects.get(t_number=name)
        except Teacher.DoesNotExist:
            return HttpResponseRedirect("/")
        if t.t_pass == ps:
            lesson = Lesson.objects.filter(l_teacher = t)
            score = Score.objects.filter(S_lesson=lesson)
            return render(request, "teacher.html", {"teacher": t, "score": score})
        else:
            return HttpResponseRedirect("/")
    else:
        return  HttpResponseRedirect("/admin/")

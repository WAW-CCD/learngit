# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from management.models import Student, Teacher,Lesson,Score,Admin
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,StreamingHttpResponse
import xlrd
import os
from django.conf import settings
import xlwt

def write_xls(request):
    t_id = request.GET.get('t_id')
    teacher = Teacher.objects.get(t_number = t_id)
    lesson = Lesson.objects.filter(l_teacher = teacher)
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('Sheet1')
    cnt = 0
    for les in lesson:
        worksheet.write(cnt, 3, les.l_name)
        cnt+=1
        score = Score.objects.filter(S_lesson = les)
        l = []
        t = 0
        for s in score:
            l.append(list())
            l[t].append(s.S_student.s_number)
            l[t].append(s.S_student.s_name)
            l[t].append(s.S_student.subject)
            l[t].append(s.S_student.grade)
            l[t].append(s.S_lesson.l_name)
            l[t].append(s.score)
            l[t].append(t+1)
            t+=1
        for i in range(0, len(l)):
            for j in range(len(l[i])):
                worksheet.write(i+cnt, j, l[i][j])
        cnt+=len(l)+1
    workbook.save('Score.xls')
    filepath = os.path.join("./", "Score.xls")
    fp = open(filepath, 'rb')
    response = StreamingHttpResponse(fp)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=Score.xls'
    return response


def download(request):
    filename = request.GET.get('file')
    filepath = os.path.join("./", filename)
    fp = open(filepath, 'rb')
    response = StreamingHttpResponse(fp)
    # response = FileResponse(fp)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % filename
    return response
    

def upload(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(
            os.path.join("./upload", myFile.name),
            'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        typ = int(request.GET.get('type'))
        if typ == 1:
            add_student(os.path.join("./upload", myFile.name))
        elif typ == 2:
            add_teacher(os.path.join("./upload", myFile.name))
        elif typ == 3:
            add_lesson(os.path.join("./upload", myFile.name))
        elif typ == 4:
            add_xuanke(os.path.join("./upload", myFile.name))
        elif typ == 5:
            add_score(os.path.join("./upload", myFile.name))
        os.remove(os.path.join("./upload", myFile.name))
        return HttpResponse("<script >alert('您已成功导入！')</script>")


def test(request):
    add_teacher(os.path.join("./test", "teacher.xls"))
    add_lesson(os.path.join("./test", "lesson.xls"))
    add_xuanke(os.path.join("./test", "xuanke.xls"))
    add_score(os.path.join("./test", "score.xls"))


# Create your views here.
def index(request):
    return render(request, "login.html")


def score_list(request):
    lesson_id = request.GET.get('lesson')
    lesson = Lesson.objects.filter(l_number = lesson_id).first()
    score = Score.objects.filter(S_lesson = lesson).order_by("-score")
    return render(request, "student_list.html", {"score": score, "lesson": lesson_id})


def change(request):
    lid = int(request.GET['lid'])
    sid = int(request.GET['sid'])
    lesson = Lesson.objects.filter(l_number = lid).first()
    student = Student.objects.filter(s_number = sid).first()
    sscore = request.POST.get("score", None)
    Score.objects.filter(S_lesson = lesson, S_student = student).update(score=sscore)
    score = Score.objects.filter(S_lesson = lesson)
    return HttpResponseRedirect("/score_list?lesson="+str(lid))

def add_student(file_path):
    Student.objects.all().delete()
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    student_list_to_insert = list()
    for x in l:
        student_list_to_insert.append(Student(s_number = x[0], s_name=x[1], grade=x[2], subject=x[3], sex=x[4], s_pass=x[5]))
    Student.objects.bulk_create(student_list_to_insert)
    #return render(request, "login.html")


def add_teacher(file_path):
    Teacher.objects.all().delete()
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    teacher_list_to_insert = list()
    for x in l:
        teacher_list_to_insert.append(Teacher(t_number = x[0], t_name=x[1], t_college=x[2], t_pass=x[3]))
    Teacher.objects.bulk_create(teacher_list_to_insert)
    #return render(request, "login.html")


def add_score(file_path):
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    student_list_to_insert = list()
    for x in l:
        Score.objects.filter(S_lesson = Lesson.objects.get(l_number = x[1]), S_student = Student.objects.get(s_number = x[0])).update(score = x[2])

def add_lesson(file_path):
    Lesson.objects.all().delete()
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    list_to_insert = list()
    for x in l:
        list_to_insert.append(Lesson(l_number = x[0], l_name=x[1], credit=x[2], l_teacher=Teacher.objects.get(t_name=x[3]), time=x[4]))
    Lesson.objects.bulk_create(list_to_insert)


def add_xuanke(file_path):
    Score.objects.all().delete()
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nrows = table.nrows
    l = (table.row_values(i) for i in range(1, nrows))
    list_to_insert = list()
    for x in l:
        list_to_insert.append(Score(S_lesson = Lesson.objects.get(l_name = x[0]), S_student = Student.objects.get(s_name = x[1])))
    Score.objects.bulk_create(list_to_insert)
    #return render(request, "login.html")


def login(request):
    print (request.POST.get("sid", None))
    if request.method == "POST":
        type = request.POST.get("fruit")
        name = request.POST.get("username", None)
        ps = request.POST.get("password", None)

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
            return render(request, "select_lesson.html", {"teacher": t, "lesson": lesson})
        else:
            return HttpResponseRedirect("/")
    else:
        try:
            A = Admin.objects.get(A_number=name)
        except Admin.DoesNotExist:
            return HttpResponseRedirect("/")
        if A.A_pass == ps:

            return render(request, "Admin.html")
        else:
            return HttpResponseRedirect("/")


def chaxun(request):
    if request.method == "POST":
        type = request.POST.get("leixing")
        name = request.POST.get("name", None)
        if type == "2":
            try:
                s = Student.objects.get(s_name=name)
            except Student.DoesNotExist:
                return HttpResponseRedirect("/")
            return render(request, "search.html", {"student": s})
        if type == "1":
            try:
                t = Teacher.objects.get(t_name=name)
            except Teacher.DoesNotExist:
                return HttpResponseRedirect("/")
            return render(request, "search_tearcher.html", {"teacher": t})
def update(request):
    if request.method == "POST":
        type = request.POST.get("leixing_update")
        name = request.POST.get("name", None)
        id = request.POST.get("id", None)
        pwd = request.POST.get("password", None)
        if type == "1":
            try:
                t = Teacher.objects.get(t_number=id)
            except Teacher.DoesNotExist:
                return HttpResponseRedirect("/")
            t.t_pass=pwd
            t.save()
            return HttpResponse("<script >alert('您已成功修改！')</script>")
        if type == "2":
            try:
                s = Student.objects.get(s_number=id)
            except Student.DoesNotExist:
                return HttpResponseRedirect("/")
            s.s_pass=pwd
            s.save()
            return HttpResponse("<script >alert('您已成功修改！')</script>")
def delete(request):
    if request.method == "POST":
        type = request.POST.get("leixing_delete")
        id = request.POST.get("id", None)
        if type == "1":
            try:
                t = Teacher.objects.get(t_number = id)
            except Teacher.DoesNotExist:
                return HttpResponseRedirect("/")
            t.detele()
            return HttpResponse("<script >alert('您已成功删除！')</script>")
        if type == "2":
            try:
                s = Student.objects.get(s_number = id)
            except Student.DoesNotExist:
                return HttpResponseRedirect("/")
            s.delete()
            return HttpResponse("<script >alert('您已成功删除！')</script>")
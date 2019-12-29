# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
    s_number = models.IntegerField(primary_key=True) #学号
    s_name = models.CharField(max_length=20)         #姓名
    sex = models.CharField(max_length=2)             #性别
    subject = models.CharField(max_length=20)        #专业
    grade = models.CharField(max_length=20)          #年级
    native_place = models.CharField(max_length=30)   #省市
    s_pass = models.CharField(max_length=33)         #密码


class Teacher(models.Model):
    t_number = models.IntegerField(primary_key=True) #工号
    t_name = models.CharField(max_length=10)         #姓名
    t_pass = models.CharField(max_length=33)         #密码
    t_college = models.CharField(max_length=40)      #学院

class Lesson(models.Model):
    l_number = models.IntegerField(primary_key=True) #课程代码
    l_name = models.CharField(max_length=30)         #课程名称
    credit = models.FloatField()                     #学分
    time = models.IntegerField()                     #学时
    l_teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE) #任课教师


class Score(models.Model):
    S_student = models.ForeignKey(Student, on_delete=models.CASCADE) #学生
    S_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)   #课程
    score = models.FloatField(null = True)                          #成绩

class Admin(models.Model):
    A_number = models.IntegerField(primary_key=True) #工号
    A_name = models.CharField(max_length=10)         #姓名
    A_pass = models.CharField(max_length=33)         #密码
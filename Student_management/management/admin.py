# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from management.models import Student,Lesson,Teacher,Score

# Register your models here.
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(Teacher)
admin.site.register(Score)


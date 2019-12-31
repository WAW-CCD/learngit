"""Student_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from management import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'change/', views.change),
    url(r'login/$', views.login),
    url(r'upload_file',views.upload),
    url(r'download',views.download),
    url(r'score_list', views.score_list),
    url(r'test', views.test),
    url(r'admin1', views.chaxun),
    url(r'admin2', views.update),
    url(r'admin3', views.delete),
	url(r'score_down', views.write_xls)
]

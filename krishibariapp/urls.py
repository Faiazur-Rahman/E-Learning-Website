from os import stat
from unicodedata import name
from django.contrib.auth import authenticate, login
from django.http.request import validate_host
from django.urls import path,re_path

from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    #path('',views.home,name='home'),
    # path('',views.add,name='haha'),
    
    #user site section
    path('login', views.log_in),
    # path('userProfile'.vi)
    path('',views.homepage),
    path('profile',views.profile),
    path('logout',views.log_out),
    path('register',views.insertrecord),
    path('coursesite',views.coursesite, name='coursesite'),
    path('onlineCourses',views.onlineCourses, name='onlineCourses'),
    # path('alltutorials',allArticlesView.as_view(), name='alltutorials'),
    # path('showarticlex',views.showArticlexView,name='showarticlex'),
    path('<int:pk>',views.showArticleView,name='showarticle'),
    path('addcomment',views.addcomment,name="addcomment"),

    #sub admin secton

    path('adminLogin',views.subadmin),
    path('subadminhome', views.index),
    path('user_list',views.user_list),
    path('courses',views.courses),
    path('userCourses',views.userCourses),
    path('newCourses',views.newCourses),
    path('addVideo',views.addVideo),
    path('courseDetails',views.courseDetails),
    path('activeState',views.activeState, name='activeState'),
    path('delVideo',views.delVideo, name='delVideo'),
    path('my_articles',views.my_articles,name='my_articles'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
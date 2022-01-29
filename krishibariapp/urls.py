from os import stat
from django.contrib.auth import authenticate, login
from django.http.request import validate_host
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    #path('',views.home,name='home'),
    # path('',views.add,name='haha'),
    path('login', views.log_in),
    # path('userProfile'.vi)
    path('',views.homepage),
    path('profile',views.profile),
    path('logout',views.log_out),
    path('register',views.insertrecord),
    path('adminLogin',views.subadmin),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
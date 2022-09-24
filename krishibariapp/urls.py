from os import stat
from unicodedata import name
from django.contrib.auth import authenticate, login
from django.http.request import validate_host
from django.urls import path, re_path

from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('',views.home,name='home'),
    # path('',views.add,name='haha'),

    # user site section
    path('login', views.log_in, name="login"),
    # path('userProfile'.vi)
    path('', views.homepage,name='home'),
    path('profile', views.profile,name='profile'),
    path('logout', views.log_out,name='logout'),
    path('register', views.insertrecord,name='register'),
    path('coursesite', views.coursesite, name='coursesite'),
    path('the-course/<int:coursePk>/<int:pk>', views.the_course, name='the-course'),
    path('onlineCourses', views.onlineCourses, name='onlineCourses'),
    # path('alltutorials',allArticlesView.as_view(), name='alltutorials'),
    # path('showarticlex',views.showArticlexView,name='showarticlex'),
    path('onlineCourse-user-registerd/<int:pk>', views.course_user_request, name='onlineCourse-user-registerd'),
    path('liveCourse-user-registered/<int:coursePk>',views.live_course_user_request,name='liveCourse-user-registered'),
    path('articles/<int:pk>', views.showArticleView, name='articles'),
    path('addcomment', views.addcomment, name="addcomment"),
    path('course-outline-online/<int:pk>', views.courseOutlineOnline, name="courseOutlineOnline"),
    path('course-outline-live/<int:coursePk>',views.courseOutlineLive,name='courseOutlineLive'),
    path('blogs', views.blogs, name="blogs"),
    path('blog-single/<int:blogPk>',views.blogSingle,name='blog-single'),
    path('blogs/write-a-blog', views.write_a_blog, name="write-a-blog"),
    path('blogs/my-blogs', views.my_blogs, name="my-blogs"),
    path('search-blogs',views.searchBlogs,name='searchBlogs'),
    path('like', views.like, name='like'),
    path('dislike', views.dislike, name='dislike'),
    path('bookmark', views.bookmark, name='bookmark'),
    path('blogs/bookmarked-blogs', views.bookmarked_blogs, name='bookmarked-blogs'),
    path('course-about', views.course_about, name='course-about'),
    path('live-courses', views.live_course, name='live-courses'),
    path('questions', views.questions, name='questions'),
    path('questions/single-question/<int:qusPk>',views.singleQuestion,name='single-question'),
    path('write-an-answer/<int:qusPk>',views.write_an_answer,name='write-an-answer'),
    path('ask-question', views.ask_question, name='ask-question'),
    path('course-test/<int:coursePk>',views.course_test,name='course-test'),
    path('course-test/<int:coursePk>/saveExam',views.course_test_save,name='course-test-save'),
    path('course-test-exam/<int:coursePk>/<int:examPk>',views.course_test_exam,name='course-test-exam'),
    path('ownProfile',views.ownProfile,name='ownProfile'),
    path('shofolUddokta',views.shofolUddokta,name='shofolUddokta'),
    path('shofolUddokta/shofolUddoktaSingle/abu-taleb',views.shofolUddoktaSingle,name='shofolUddoktaSingle'),
    path('marketPlaces',views.marketPlaces,name='marketPlaces'),

    # sub admin secton

    path('pending_to_active/<int:course_pk>/<int:stu_pk>/<int:sid>',views.pending_to_active,name='pending_to_active'),
    path('adminLogin', views.subadmin,name='adminLogin'),
    path('subadminhome', views.index,name='subadminhome'),
    path('user_list', views.user_list,name='user_list'),
    path('courses', views.courses, name='courses'),
    path('userCourses', views.userCourses,name='userCourses'),
    path('newCourses', views.newCourses, name='newCourses'),
    path('onlineCourseDetails', views.courseDetails,name='onlineCourseDetails'),
    path('liveCourseDetails',views.liveCourseDetails,name='liveCourseDetails'),
    path('activeState', views.activeState, name='activeState'),
    path('delVideo', views.delVideo, name='delVideo'),
    path('my_articles', views.my_articles, name='my_articles'),
    path('question-admin',views.question_admin,name='question-admin'),
    path('approve-question',views.approve_question,name='approve-question'),
    path('liveCourseLinkSend/<int:course_pk>',views.liveCourseLinkSend,name='liveCourseLinkSend'),
    path('view-question/<int:pk>',views.view_question,name='view-question'),
    path('the-course-admin/<int:pk>',views.the_course_admin,name='the-course-admin'),
    path('the-live-course-admin/<int:pk>',views.the_live_course_admin,name='the-live-course-admin'),
    # instructor section
    path('instructor-login', views.instructor_login,name='instructorLogin'),
    path('instructor-home', views.instructor_home,name='instructor-home'),
    path('instructor-course',views.instructor_course,name='instructor-course'),
    path('instructor-the-course/<int:pk>',views.instructor_the_course,name='instructor_the_course'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


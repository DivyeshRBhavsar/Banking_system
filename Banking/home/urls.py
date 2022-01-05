from django.urls import path
from . import views
from django.contrib import admin


urlpatterns=[

    path('',views.home, name='home'),
    path('show_home',views.show_home,name='show_home'),
    path('loginprocess',views.loginprocess, name='loginprocess'),
    path('show_signup',views.show_signup,name='show_signup'),
    path('profileuser',views.profileuser,name='profileuser'),
    path('logout',views.logoutprocess,name='logoutprocess'),


]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),

    # User 관련 API
    path('users/login', views.login, name="login"),
    path('users/createexercise', views.createexercise, name="createexercise"),
    path('users/createmotion', views.createmotion, name="createmotion"),
    path('users/getuserexercise', views.getuserexercise, name="getuserexercise"),
    path('users/getuserfeedback', views.getuserfeedback, name="getuserfeedback"),

    # Image 관련 API
    path('images/saveimage', views.saveimage, name="saveimage"),
    path('images/getjointpoint', views.getjointpoint, name='getjointpoint'),
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),

    # User 관련 API
    path('users/register', views.register, name="register"),
    path('users/login', views.login, name="login"),
    path('users/createexercise', views.createexercise, name="createexercise"),
    path('users/getuserexercise', views.getuserexercise, name="getuserexercise"),
    path('users/getuserfeedback', views.getuserfeedback, name="getuserfeedback"),

    # Image 관련 API
    path('images/getjointpoint', views.getjointpoint, name='getjointpoint'),
]
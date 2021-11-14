from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),

    # User 관련 API
    path('users/login', views.login, name="login"),
    path('users/getexercise', views.getuserexercise, name="getuserexercise"),
    path('users/getfeedback', views.getuserfeedback, name="userfeedback"),

    # Image 관련 API
    path('images/', views.getimages, name="getimages"),
    path('images/getjointpoint', views.getjointpoint, name='getjointpoint'),
]
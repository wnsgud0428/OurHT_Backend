from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('users/login', views.login, name="login"),
    #path('images/', views.getImages, name="getImages"),
]
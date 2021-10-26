from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes, name="routes"),
    path("users/", views.getUsers, name="getUsers"),
    path("images/", views.getImages, name="getImages"),
    path("images/getjointpoint", views.getjointpoint, name="getjointpoint"),
]

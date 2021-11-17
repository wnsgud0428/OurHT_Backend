from django.urls import path
from . import views

# 로그인을 위해
from django.conf.urls import include
from rest_framework import routers
from .views import UserViewSet, MotionViewSet, ExerciseList

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("motions", MotionViewSet)
###

urlpatterns = [
    ###로그인을 위해
    path("", include(router.urls)),
    path("exercises/", views.ExerciseList, name="getExerciseList"),
    ###
    path("", views.getRoutes, name="routes"),
    # User 관련 API
    path("users/login", views.login, name="login"),
    path("users/getuserinfo", views.getuserinfo, name="getuserinfo"),
    # Image 관련 API
    path("images/", views.getimages, name="getimages"),
    path("images/getjointpoint", views.getjointpoint, name="getjointpoint"),
]

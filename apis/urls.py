from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),

    # User 관련 API
    path('users/login', views.login, name="login"),
    path('users/getuserinfo', views.getuserinfo, name='getuserinfo'),
    
    # 
    #path('images/', views.getImages, name="getImages"),
]
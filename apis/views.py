from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
# 주석 달기, body 부분 수정
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/users/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of users'
        },
        {
            'Endpoint': '/users/',
            'method': 'POST',
            'body': None,
            'description': 'Create User'
        }
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
# 'api/users/login' - 유저 로그인 기능 처리 함수
def login(request):
    # GET 요청 처리 -> 
    if request.method == 'GET':
        data = request.data

    # POST 요청 처리
    if request.method == 'POST':
        pass
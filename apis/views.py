from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
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
        # data = request.data
        pass

    # POST 요청 처리
    if request.method == 'POST':
        data = request.data
        pass
    
    # 로그인 함수 로직 -> 위의 GET , POST 요청 고민해서 로직 넣어야함!
    input_id = data["userid"]
    input_password = data["userpassword"]
    user = User.objects.filter(userid = input_id, userpassword = input_password)
    user_2 = User.objects.filter(userid = input_id)
    if not user and user_2:
        # 아이디는 존재하나, 비밀번호 오류
        print("비번 오류")
    elif not user and not user_2:
        # 로그인 실패
        print("로그인 실패")
    else:
        # 로그인 성공
        print("Success")
    
    # Response 응답 고민!
    return Response("응답을 뭘 줄껀지도 고민")

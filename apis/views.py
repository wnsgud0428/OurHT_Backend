from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import UserSerializer
from .models import User
# Create your views here.

@api_view(['GET'])
# 주석 달기
def getRoutes(request):

    routes = [
        {
            # 'api/users/login'
            'Endpoint': 'api/users/login',
            'method': 'GET', 'POST'
            'body': {"userid", "userpassword"},
            'description': '로그인 성공 여부 판단'
        },
        {
            # 'api/users/getuserinfo'
            'Endpoint': 'api/users/getuserinfo',
            'method': 'GET',
            'body': {'username'},
            'description': '유저 이름을 받아, 유저 정보 웹으로 전달'
        },
        {
            # 'api/images
        },
        {
            # API 만들때마다 추가
        }
    ]
    return Response(routes)

# 'api/users/login' - 유저 로그인 기능 처리 함수
@api_view(['GET', 'POST'])
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

# 'api/users/getuserinfo' - 유저 정보를 웹에 전달해주는 함수
@api_view(['GET'])
def getuserinfo(request):

    username = request.GET.get("username")
    user = User.objects.filter(username=username)

    if not user:
        # 유저 존재안함! 요청 오류
        pass
    else:
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

# 'api/images/getjointpoint' - 관절포인트가 담긴 정보를 웹에서 받아오는 함수
@api_view(['POST'])
def getjointpoint(request):
    # POST 요청 처리
    if request.method == 'POST':
        data = request.data
        print(data)
        return Response("데이터 잘 받았습니다.")

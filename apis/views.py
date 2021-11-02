from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import UserSerializer
from .models import User

import base64

# Create your views here.


@api_view(["GET"])
# 주석 달기
def getRoutes(request):

    routes = [
        {
            # 'apis/users/login'
            "Endpoint": "api/users/login",
            "method": "GET",
            "POST" "body": {"userid", "userpassword"},
            "description": "로그인 성공 여부 판단",
        },
        {
            # 'apis/users/getuserinfo'
            "Endpoint": "api/users/getuserinfo",
            "method": "GET",
            "body": {"username"},
            "description": "유저 이름을 받아, 유저 정보 웹으로 전달",
        },
        {
            # 'apis/images
        },
        {
            # 'apis/images/getjointpoint
        },
        {
            # API 만들때마다 추가
        },
    ]
    return Response(routes)


# 'apis/users/login' - 유저 로그인 기능 처리 함수
@api_view(["GET", "POST"])
def login(request):
    # GET 요청 처리 ->
    if request.method == "GET":
        # data = request.data
        pass

    # POST 요청 처리
    if request.method == "POST":
        data = request.data
        pass

    # 로그인 함수 로직 -> 위의 GET , POST 요청 고민해서 로직 넣어야함!
    input_id = data["userid"]
    input_password = data["userpassword"]
    user = User.objects.filter(userid=input_id, userpassword=input_password)
    user_2 = User.objects.filter(userid=input_id)
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


# 'apis/users/getuserinfo' - 유저 정보를 웹에 전달해주는 함수
@api_view(["GET"])
def getuserinfo(request):

    username = request.GET.get("username")
    user = User.objects.filter(username=username)

    if not user:
        # 유저 존재안함! 요청 오류
        pass
    else:
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


# 'apis/images' - 유저의 운동이미지를 받아와서 저장하는 함수
@api_view(["GET", "POST"])
def getimages(request):

    # 'api/images'으로 온 POST 요청 처리 -> Image 객체 생성
    if request.method == "POST":
        print("Images POST")
        # POST로 온 데이터 받기
        data = request.data
        # data 앞에 쓸모없는 문자열 제거
        replace_data = data.replace("data:image/jpeg;base64,", "")
        # 이미지파일로 디코딩한후, 파일에 이미지 데이터 쓰기
        imgdata = base64.b64decode(replace_data)
        with open("media/test.jpg", "wb") as f:
            f.write(imgdata)

        # 데이터 여러개 받아오는 경우
        """
        data = request.data
        # base64를 이미지로 바꾸는 과정, test.jpeg에 저장
        imgdata = base64.b64decode(data["url"])
        with open('test.jpeg', 'wb') as f:
            f.write(imgdata)
        """
        # 이미지 모델 저장은 조금 더 고민..
        # image = Image.objects.create(image_url = binary_data)
        # serializer = ImageSerializer(image, many=False)
    return Response()


# 'apis/images/getjointpoint' - 관절포인트가 담긴 정보를 웹에서 받아오는 함수
@api_view(["POST"])
def getjointpoint(request):
    # POST 요청 처리
    if request.method == "POST":
        left_shoulder_x = request.data["keypoints"][5]["position"]["x"]
        right_shoulder_x = request.data["keypoints"][6]["position"]["x"]
        diff = abs(left_shoulder_x - right_shoulder_x)

        left_ankle_x = request.data["keypoints"][15]["position"]["x"]
        left_ankle_y = request.data["keypoints"][15]["position"]["y"]

        # 발목 보이는거를 위해
        len = 480 - left_ankle_y
        print(len)
        if len > 30:
            print("발목이 보여요!")

        # 중앙 정렬을 위해
        # print(left_ankle_x)
        # if 250 < left_ankle_x < 390:
        #     print("중앙정렬 완료")
        # else:
        #     print("너무 쳐져있어요!")

        # 측면정렬을 위해
        # print(diff)
        if diff < 20:
            # print("옆으로 잘 섰네요")
            return Response("측면정렬 완료!")
        return Response("측면정렬 미완료!")

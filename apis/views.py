from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import UserSerializer
from .models import User
from . import feedback
import base64
from .camera_feedback import isCameraSetted
from .pose_feedback import isFaceForward, isUpperbodyNotBent
from .squat_state_check import returnSquatState
from pose import models as pose_models

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
# dynamic_data - 동적인 데이터 위해
"""
dynamic_data = []
count = 0
"""

pose_list = []
feedback_result = []
is_person_gone_to_stand = "no"

@api_view(["POST"])
def getjointpoint(request):

    global is_person_gone_to_stand

    # POST 요청 처리
    if request.method == "POST":
        camSetFlag = isCameraSetted(request)

        if camSetFlag == True:
            data = request.data
            squat_state = returnSquatState(data)

            if squat_state == "squat":
                pose_list.append(data)
                is_person_gone_to_stand = "no"
            else:
                if squat_state == "stand":
                    is_person_gone_to_stand = "yes"

                if is_person_gone_to_stand == "yes":
                    # pose_list 처리 하는 부분
                    pose_list_for_hip_y = []
                    for p in pose_list:
                        pose_list_for_hip_y.append(p["keypoints"][11]["position"]["y"])
                    # print(pose_list_for_hip_y)
                    if pose_list_for_hip_y:
                        max_hip_y = max(pose_list_for_hip_y)

                        # 샘플링 할 사진 index 찾기
                        for i in range(len(pose_list_for_hip_y)):
                            if max_hip_y == pose_list_for_hip_y[i]:
                                max_hip_y_index = i

                        #print(f"hip_y의 리스트:{pose_list_for_hip_y}")
                        #print(f"max_hip_y 값:{max_hip_y}")

                        # 샘플링 사진으로 피드백 함수 돌리기
                        data = pose_list[max_hip_y_index]
                        feedback_result.append(isUpperbodyNotBent(request))
                        feedback_result.append(isFaceForward(request))  # 수정 필요, 각도가 크게 안바뀜, 왼오른쪽 방향도 중요
                        feedback_result.append(feedback.checkRangeofmotion(data))
                        feedback_result.append(feedback.checkKneeposition(data))
                        feedback_result.append(feedback.checkCenterofgravity(data))
                        # OpenCV 등 피드백 함수 추가

                        # DB에 결과 저장 및 변수 초기화
                        # 모델 완성되는대로 추가해야함!
                        # ~.objects.create(### = feedback_result[i])
                        pose_models.Pose.objects.create(hip_y=max_hip_y)
                        pose_list_for_hip_y.clear()
                        pose_list.clear()

                        # 실시간 피드백을 위한 응답 
                        feedback_true_count = 0
                        for f in feedback_result:
                            if f == "True":
                                feedback_true_count += 1
                        
                        if feedback_true_count >= 5:
                            return Response("Perfect")
                        elif feedback_true_count <= 1:
                            return Response("Bad")
                        else:
                            return Response("Good")
                else:
                    pass
        else:
            return Response("카메라 세팅 다시 하세요")

from typing import Tuple
from django.db.models import query
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users import serializer as user_serializer
from exercises import serializer as exercise_serializer
from users import models as user_models
from exercises import models as exercise_models
import base64
from .camera_feedback import isCameraSetted
from .pose_feedback import isFaceForward, isUpperbodyNotBent
from .squat_state_check import returnSquatState

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
    user = user_models.User.objects.filter(userid=input_id, userpassword=input_password)
    user_2 = user_models.User.objects.filter(userid=input_id)
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


# 'apis/users/getexercise' - Exercise 모델을 웹에 전달해주는 함수
@api_view(["GET"])
def getuserexercise(request):
    if request.method == 'GET':
        username = request.GET.get("username")
        print(username)
        user = user_models.User.objects.get(username=username)
        if not user:
            # 유저 존재안함! 요청 오류
            pass
        else:
            queryset = exercise_models.Exercise.objects.get(user = user.id)
            # 1개인 경우, 여러개인 경우 구분!
            serializer = exercise_serializer.ExerciseSerializer(queryset, many=False)
            print(serializer.data)
            return Response(serializer.data)

# 'apis/users/getfeedback - 자세한 피드백을 위해 유저 피드백 내용을 들고와 웹에 뿌려주는 API
@api_view(['GET'])
def getuserfeedback(request):
    if request.method == 'GET':
        username = request.GET.get("username")
        user = user_models.User.objects.get(username = username)
        if not user:
            # 찾고자 유저 없는 경우
            pass
        else:
            # 유저를 알았으니, 그 유저에 맞는 피드백 찾기
            queryset = exercise_models.Motion.objects.filter(
            exercise = exercise_models.Exercise.objects.get(user = user.id))
            serializer = exercise_serializer.MotionSerializer(queryset, many=True)
            return Response(serializer.data)
    '''
    #장고 ORM에서 찾을때,
    queryset = exercise_models.Motion.objects.filter(
        exercise = exercise_models.Exercise.objects.get(user = 1))
    )
    '''

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

# dynamic_data - 동적인 데이터 위해
"""
dynamic_data = []
count = 0
"""

pose_list = []
is_person_gone_to_stand = "no"

# 'apis/images/getjointpoint' - 관절포인트가 담긴 정보를 웹에서 받아오는 함수
@api_view(["POST"])
def getjointpoint(request):
    global is_person_gone_to_stand
    # POST 요청 처리
    if request.method == "POST":
        # 준형
        camSetFlag = isCameraSetted(request)
        # isUpperbodyNotBent(request)  # 테스트 완료
        # isFaceForward(request)  # 수정 필요, 각도가 크게 안바뀜, 왼오른쪽 방향도 중요

        # 병주
        data = request.data
        # RangeofmotionFlag = feedback.checkRangeofmotion(data) #잘됨
        # KneepositionFlag = feedback.checkKneeposition(data) #잘됨
        # CenterofgraityFlag = feedback.checkCenterofgravity(data) #잘됨

        if camSetFlag == True:
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
                        print(f"hip_y의 리스트:{pose_list_for_hip_y}")
                        print(f"max_hip_y 값:{max_hip_y}")
                        pose_models.Pose.objects.create(hip_y=max_hip_y)
                        pose_list_for_hip_y.clear()
                        pose_list.clear()
                else:
                    pass

        if camSetFlag == True:
            return Response(" ")
        else:
            return Response("카메라 세팅 다시 하세요")

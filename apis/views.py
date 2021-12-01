import cv2, numpy, util, base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users import serializer as user_serializer
from exercises import serializer as exercise_serializer
from users import models as user_models
from exercises import models as exercise_models
from .camera_feedback import isCameraSetted
from .squat_state_check import returnSquatState
from . import feedback
from PIL import Image

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

# 'apis/users/register - 유저 회원가입 기능 처리 함수
@api_view(["POST"])
def register(request):
    if request.method == "POST":
        username = request.data["username"]
        password = request.data["password"]

        user = user_models.User.objects.filter(username=username)
        if not user:
            user = user_models.User.objects.create_user(username=username, password=password)
            print(user.pk)
            return Response(user.pk)
        else:
            return Response(-1)

# 'apis/users/login' - 토큰 통해 유저 로그인 기능 처리 함수
@api_view(["POST"])
def login(request):
    if request.method == "POST":
        usertoken = request.data["usertoken"]
        print(usertoken)
        token = Token.objects.get(key=usertoken)
        return Response(token.user.id)

# 'apis/users/createexercise' - Exercise 모델 생성, 생성된 모델의 PK를 응답함
@api_view(["POST"])
def createexercise(request):
    if request.method == "POST":
        userid = request.data["userid"]
        user = user_models.User.objects.get(id=userid)
        create_exercise = exercise_models.Exercise.objects.create(user=user, type="squat")
        return Response(create_exercise.pk)

# 'apis/users/getexercise' - Exercise 모델을 웹에 전달해주는 함수
@api_view(["GET"])
def getuserexercise(request):
    if request.method == "GET":
        username = request.GET.get("username")
        user = user_models.User.objects.get(username=username)
        if not user:
            return Response("User Does Not Exist")
        else:
            queryset = exercise_models.Exercise.objects.get(user=user.id)
            if len(queryset) >= 2:
                serializer = exercise_serializer.ExerciseSerializer(queryset, many=True)
            else:
                serializer = exercise_serializer.ExerciseSerializer(
                    queryset, many=False
                )
            return Response(serializer.data)


# 'apis/users/getuserfeedback - 자세한 피드백을 위해 유저 피드백 내용(Motion 모델)을 들고와 웹에 뿌려주는 API
save_data = []

@api_view(["GET"])
def getuserfeedback(request):

    if request.method == "GET":
        exercise_pk = request.GET.get("exercise_pk")
        motion_index = request.GET.get("motion_index")
        print(exercise_pk, motion_index)
        exercise = exercise_models.Exercise.objects.get(pk = exercise_pk)

        if not exercise:
            return Response("Exercise Does Not Exist")
        else:
            # 유저를 알았으니, 그 유저에 맞는 피드백 찾기
            queryset = exercise_models.Motion.objects.filter(exercise=exercise)

            for i in range(len(queryset)):
                # Motion 모델을 보고 등 분석이 진행이 안돼어 있을 시, 등 분석 진행!
                if queryset[i].feedback_check == False:
                    image_data = queryset[i].photo
                    temp = base64.b64decode(image_data)
                    with open("photos/test2.webp", "wb") as f:
                        f.write(temp)
                    f.close()

                    im = Image.open('photos/test2.webp').convert('RGB')
                    im.save('photos/test2.jpg', 'jpeg')

                    with open("photos/test2.jpg","rb") as f:
                        encode_str = base64.b64encode(f.read())

                    rmbg = util.NewRemoveBg("yLhTTo4uCPsYtMAyqFviYCKN", "error.log")
                    rmbg.remove_background_from_base64_img(encode_str)

                    image_arr = cv2.imread("photos/no-bg.png", 1)
                    image_arr = numpy.array(image_arr)

                    # 등 분석 함수 진행, 관절 포인트는 전역 변수 - save_data 배열로 받아옴
                    backlineflag = feedback.checkbackline(save_data[i], image_arr)
                    if backlineflag == True:
                        queryset[i].checklist.add(3)
                    # 바로 값이 바뀌나?
                    queryset[i].feedback_check = True
                    queryset[i].save()

            # 변수 초기화
            save_data.clear()

            if motion_index == "999":
                serializer = exercise_serializer.MotionSerializer(queryset, many=True)
            else:
                queryset = queryset[int(motion_index) - 1]
                serializer = exercise_serializer.MotionSerializer(queryset, many=False)
            return Response(serializer.data) 


# 'apis/images/getjointpoint' - 관절포인트가 담긴 정보를 웹에서 받아오는 함수
feedback_result = []

@api_view(["POST"])
def getjointpoint(request):

    # 프론트와 분리한 새 버전
    print("Hello New Function")
    data = request.data["skeletonpoint"]
    count = request.data["count"]
    image_data = request.data["url"].replace("data:image/webp;base64,", "")

    feedback_result.append(feedback.isUpperbodyNotBent(data))
    feedback_result.append(feedback.isFaceForward(data))  # 수정 필요, 각도가 크게 안바뀜, 왼오른쪽 방향도 중요
    feedback_result.append(feedback.checkRangeofmotion(data))
    feedback_result.append(feedback.checkKneeposition(data))
    feedback_result.append(
        feedback.checkCenterofgravity(data)
    )  # 무게중심 깐깐함
    print("피드백 결과 : ", feedback_result)

    save_data.append(data)

    # DB에 결과 저장
    print(request.data["exercise_pk"])
    exercise_pk = request.data["exercise_pk"]
    exercise = exercise_models.Exercise.objects.get(pk = exercise_pk)
    create_motion = exercise_models.Motion.objects.create(
        exercise=exercise, count_number=count, photo=image_data
    )

    # 생성한 Motion 모델에 피드백 결과 checklist 넣기
    for i in range(len(feedback_result)):
        if feedback_result[i] == True:
            create_motion.checklist.add(i + 1)
    create_motion.save()

    # 실시간 피드백을 위한 응답
    feedback_true_count = 0
    for f in feedback_result:
        if f == True:
            feedback_true_count += 1

    # 변수 초기화
    feedback_result.clear()

    # 결과
    print("결과 : ", count, feedback_true_count)
    if feedback_true_count >= 4:
        return Response("Perfect")
    elif feedback_true_count <= 1:
        return Response("Bad")
    else:
        return Response("Good")
import cv2, numpy, util
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
from . import feedback

# Create your views here.

count = 1


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


# 'apis/users/createexercise' - Exercise 모델 생성, 생성된 모델의 PK를 응답함
@api_view(["POST"])
def createexercise(request):
    if request.method == "POST":
        # userid = request.data["userid"]
        user = user_models.User.objects.get(id=1)
        create_exercise = exercise_models.Exercise.objects.create(user=user, type=1)
        return Response(create_exercise.pk)


# 'apis/users/createmotion' - Motion 모델 생성, 생성된 모델의 PK를 응답함 // 필요 없을 듯?
@api_view(["POST"])
def createmotion(request):
    if request.method == "POST":
        exercise_pk = request.data["exercisepk"]
        count_number = request.data["countnumber"]
        create_motion = exercise_models.Motion.objects.create(
            exercise=exercise_pk, count_number=count_number, checklist=None, photo=None
        )
        return Response(create_motion.pk)


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
    # 운동이 끝나서 이 함수가 호출되므로, count 변수 초기화!
    global count
    count = 1

    if request.method == "GET":
        #username = request.GET.get("username")
        #date = request.GET.get("date")
        #user = user_models.User.objects.get(username=username)

        exercise_pk = request.GET.get("exercise_pk")
        exercise = exercise_models.Exercise.objects.get(pk = exercise_pk)
        '''
        if not user:
            return Response("User Does Not Exist")
        else:
            # 유저를 알았으니, 그 유저에 맞는 피드백 찾기
            queryset = exercise_models.Motion.objects.filter(
                exercise=exercise_models.Exercise.objects.get(
                    user=user.id, created=date
                )
            )
        '''
        if not exercise:
            return Response("Exercise Does Not Exist")
        else:
            # 유저를 알았으니, 그 유저에 맞는 피드백 찾기
            queryset = exercise_models.Motion.objects.filter(exercise=exercise)

            for i in range(len(queryset)):
                # Motion 모델을 보고 등 분석이 진행이 안돼어 있을 시, 등 분석 진행!
                if queryset[i].feedback_check == False:
                    # 모델에서 이미지 가져오기 - 배경 제거도 해야함
                    image_data = queryset[i].photo
                    rmbg = util.NewRemoveBg(util.API_KEY, "error.log")
                    image_arr = rmbg.remove_background_from_base64_img(image_data)
                    """
                    # 배경 제거 후
                    image_arr = base64.b64decode(image_data)
                    with open('images/test.jpeg', 'wb') as f:
                        f.write(image_arr)
                    f.close()
                    image_arr = cv2.imread('test.jpeg', 1)
                    image_arr = numpy.array(image_arr)
                    """
                    # 등 분석 함수 진행, 관절 포인트는 전역 변수 - save_data 배열로 받아옴
                    backlineflag = feedback.checkbackline(save_data[i], image_arr)
                    if backlineflag == True:
                        queryset[i].checklist.add(
                            exercise_models.Checklist.objects.get(pk=6)
                        )
                    # 바로 값이 바뀌나?
                    queryset[i].feedback_check = True

            # 변수 초기화
            save_data.clear()

            if len(queryset) >= 2:
                serializer = exercise_serializer.MotionSerializer(queryset, many=True)
            else:
                serializer = exercise_serializer.MotionSerializer(queryset, many=False)
            print(serializer.data)
            return Response(serializer.data)


# 'apis/images/saveimages' - 유저의 운동이미지를 받아와서 저장하는 함수
@api_view(["POST"])
def saveimage(request):
    # 'api/images'으로 온 POST 요청 처리 -> Image 객체 생성
    if request.method == "POST":
        exercise_pk = request.data["exercisepk"]
        count_number = request.data["countnumber"]
        image_url = request.data["url"]
        image_data = image_url.replace("data:image/jpeg;base64,", "")
        image_data = base64.b64decode(image_data)

        queryset = exercise_models.Motion.objects.filter(
            exercise=exercise_models.Exercise.objects.get(pk=exercise_pk),
            count_number=count_number,
        )
        queryset.update(photo=image_data)
    return Response()


# 'apis/images/getjointpoint' - 관절포인트가 담긴 정보를 웹에서 받아오는 함수

pose_list = []
url_list = []
feedback_result = []
is_person_gone_to_stand = "no"


@api_view(["POST"])
def getjointpoint(request):

    global is_person_gone_to_stand, count
    data = request.data["skeletonpoint"]
    image_url = request.data["url"]

    if request.method == "POST":
        # 카메라 세팅 체크
        camSetFlag = isCameraSetted(data)
        if camSetFlag == True:
            # 현재 스쿼트 상태 체크
            squat_state = returnSquatState(data)
            # 스쿼트 상태인 경우, 샘플링을 위해 데이터 수집
            if squat_state == "squat":
                pose_list.append(data)
                url_list.append(image_url)
                is_person_gone_to_stand = "no"
            else:
                if squat_state == "stand":
                    is_person_gone_to_stand = "yes"
                # 스쿼트를 한번 한 후, 다시 일어난 경우
                if is_person_gone_to_stand == "yes":
                    # 스쿼트 사진 중에서, 가장 제대로 앉은 사진 샘플링하기
                    pose_list_for_hip_y = []
                    for p in pose_list:
                        pose_list_for_hip_y.append(p["keypoints"][11]["position"]["y"])
                    if pose_list_for_hip_y:
                        max_hip_y = max(pose_list_for_hip_y)
                        # 샘플링 할 사진 index 찾기, 이미지 url도 저장하기
                        for i in range(len(pose_list_for_hip_y)):
                            if max_hip_y == pose_list_for_hip_y[i]:
                                max_hip_y_index = i

                        # 사진 샘플링
                        sampling_data = pose_list[max_hip_y_index]
                        # 등 분석을 위해 관절 포인트 전역변수에 저장
                        save_data.append(sampling_data)
                        # URL 샘플링
                        image_data = url_list[max_hip_y_index].replace(
                            "data:image/webp;base64,", ""
                        )
                        """
                        image_arr = base64.b64decode(image_data)
                        with open("test.jpeg", "wb") as f:
                            f.write(image_arr)
                        f.close()
                        image_arr = cv2.imread('test.jpeg', 1)
                        image_arr = numpy.array(image_arr)

                        # 간단한 방법?
                        #image_arr = numpy.fromstring(base64.b64decode(image_data), numpy.uint8)
                        """
                        feedback_result.append(isUpperbodyNotBent(sampling_data))
                        feedback_result.append(
                            isFaceForward(sampling_data)
                        )  # 수정 필요, 각도가 크게 안바뀜, 왼오른쪽 방향도 중요
                        feedback_result.append(feedback.checkRangeofmotion(sampling_data))
                        feedback_result.append(feedback.checkKneeposition(sampling_data))
                        feedback_result.append(
                            feedback.checkCenterofgravity(sampling_data)
                        )  # 무게중심 깐깐함
                        print("피드백 결과 : ", feedback_result)

                        # DB에 결과 저장
                        # exercise_pk = request.data["exercisepk"]
                        exercise = exercise_models.Exercise.objects.get(pk=1)
                        create_motion = exercise_models.Motion.objects.create(
                            exercise=exercise, count_number=count, photo=image_data
                        )
                        # 생성한 Motion 모델에 피드백 결과 checklist 넣기
                        for i in range(len(feedback_result)):
                            if feedback_result[i] == "True":
                                create_motion.checklist.add(
                                    exercise_models.Checklist.objects.get(pk=i)
                                )

                        # 실시간 피드백을 위한 응답
                        feedback_true_count = 0
                        for f in feedback_result:
                            if f == True:
                                feedback_true_count += 1

                        # 변수 초기화
                        pose_list_for_hip_y.clear()
                        pose_list.clear()
                        feedback_result.clear()
                        count += 1

                        print("결과 : ", count, feedback_true_count)
                        if feedback_true_count >= 4:
                            return Response("Perfect")
                        elif feedback_true_count <= 1:
                            return Response("Bad")
                        else:
                            return Response("Good")
                else:
                    pass
            return Response("운동 진행 중")
        else:
            return Response("카메라 세팅 다시 하세요")

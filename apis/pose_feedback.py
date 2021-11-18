from util import calculate_angle


def isUpperbodyNotBent(data):
    is_upperbody_not_bent = False

    left_shoulder_x = data["keypoints"][5]["position"]["x"]
    left_shoulder_y = data["keypoints"][5]["position"]["y"]
    right_shoulder_x = data["keypoints"][6]["position"]["x"]
    right_shoulder_y = data["keypoints"][6]["position"]["y"]

    left_hip_x = data["keypoints"][11]["position"]["x"]
    left_hip_y = data["keypoints"][11]["position"]["y"]
    right_hip_x = data["keypoints"][12]["position"]["x"]
    right_hip_y = data["keypoints"][12]["position"]["y"]

    left_knee_x = data["keypoints"][13]["position"]["x"]
    left_knee_y = data["keypoints"][13]["position"]["y"]
    right_knee_x = data["keypoints"][14]["position"]["x"]
    right_knee_y = data["keypoints"][14]["position"]["y"]

    # left_ankle_x = data["keypoints"][15]["position"]["x"]
    # left_ankle_y = data["keypoints"][15]["position"]["y"]

    shoulder_x = (left_shoulder_x + right_shoulder_x) / 2
    shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
    hip_x = (left_hip_x + right_hip_x) / 2
    hip_y = (left_hip_y + right_hip_y) / 2
    knee_x = (left_knee_x + right_knee_x) / 2
    knee_y = (left_knee_y + right_knee_y) / 2

    shoulder = [shoulder_x, shoulder_y]
    hip = [hip_x, hip_y]
    knee = [knee_x, knee_y]
    # left_ankle = [left_ankle_x, left_ankle_y]

    shoulder_hip_knee_angle = calculate_angle(shoulder, hip, knee)
    # hip_knee_ankle_angle = calculate_angle(left_hip, left_knee, left_ankle)

    ### 발목의 중앙 정렬을 위해 --> 정확도 향상을 하려면 left_ankle뿐만 아니라 right_ankle도 고려해야됨
    # print(f"어깨-엉덩이-무릎 각도:{shoulder_hip_knee_angle}")
    # print(f"엉덩이-무릎-발목 각도:{hip_knee_ankle_angle}")

    if 35 < shoulder_hip_knee_angle < 90:
        is_upperbody_not_bent = True
        print("2-3: 적당하게 숙인 각도에요")
    elif shoulder_hip_knee_angle <= 35:
        is_upperbody_not_bent = False
        print("너무 굽었어요!")
    elif shoulder_hip_knee_angle >= 180:
        is_upperbody_not_bent = None
        print("몸을 뒤로 제끼면 안되죠!")

    if is_upperbody_not_bent == True:
        return True
    else:
        return False


# 눈-귀-어깨 각도 비교
def isFaceForward(data):
    is_face_forward = False

    nose_x = data["keypoints"][0]["position"]["x"]
    nose_y = data["keypoints"][0]["position"]["y"]

    left_ear_x = data["keypoints"][3]["position"]["x"]
    left_ear_y = data["keypoints"][3]["position"]["y"]
    right_ear_x = data["keypoints"][4]["position"]["x"]
    right_ear_y = data["keypoints"][4]["position"]["y"]

    nose = [nose_x, nose_y]
    left_ear = [left_ear_x, left_ear_y]
    right_ear = [right_ear_x, right_ear_y]
    extra_point = []
    ear_nose_extra_angle = 0

    if returnPersonFaceDirection(data) == "right face is front":
        print("right face is front")  # test
        extra_point = [right_ear_x, nose_y]
        ear_nose_extra_angle = calculate_angle(right_ear, nose, extra_point)
    elif returnPersonFaceDirection(data) == "left face is front":
        print("left face is front")  # test
        extra_point = [left_ear_x, nose_y]
        ear_nose_extra_angle = calculate_angle(right_ear, nose, extra_point)

    print(ear_nose_extra_angle)  # test
    if ear_nose_extra_angle < 40:  # todo: 값 수정
        is_face_forward = True

    if is_face_forward == True:
        return True
    else:
        return False


def returnPersonFaceDirection(data):
    """사람이 어느쪽으로 서있는지 return함"""
    left_eye_x = data["keypoints"][1]["position"]["x"]
    right_eye_x = data["keypoints"][2]["position"]["x"]
    nose_x = data["keypoints"][0]["position"]["x"]

    if left_eye_x < nose_x and right_eye_x < nose_x:
        return "right face is front"
    else:
        return "left face is front"

import util, numpy as np

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

    shoulder = [(left_shoulder_x + right_shoulder_x) / 2, (left_shoulder_y + right_shoulder_y) / 2]
    hip = [(left_hip_x + right_hip_x) / 2, (left_hip_y + right_hip_y) / 2]
    knee = [(left_knee_x + right_knee_x) / 2, (left_knee_y + right_knee_y) / 2]

    shoulder_hip_knee_angle = util.calculate_angle(shoulder, hip, knee)

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
    ear_nose_extra_angle = 0

    if returnPersonFaceDirection(data) == "right face is front":
        print("right face is front")  # test
        ear_nose_extra_angle = util.calculate_angle(right_ear, nose, [right_ear_x, nose_y])
    elif returnPersonFaceDirection(data) == "left face is front":
        print("left face is front")  # test
        ear_nose_extra_angle = util.calculate_angle(left_ear, nose, [left_ear_x, nose_y])

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

def checkRangeofmotion(data):
    # 좌표 받아오기
    left_waist = data["keypoints"][11]["position"]
    right_waist = data["keypoints"][12]["position"]
    left_knee = data["keypoints"][13]["position"]
    right_knee = data["keypoints"][14]["position"]
    left_ankle = data["keypoints"][15]["position"]
    right_ankle = data["keypoints"][16]["position"]

    # 관절 좌, 우 중심점 찾기
    waist = [
        (left_waist["x"] + right_waist["x"]) / 2,
        (left_waist["y"] + right_waist["y"]) / 2,
    ]
    knee = [
        (left_knee["x"] + right_knee["x"]) / 2,
        (left_knee["y"] + right_knee["y"]) / 2,
    ]
    ankle = [
        (left_ankle["x"] + right_ankle["x"]) / 2,
        (left_ankle["y"] + right_ankle["y"]) / 2,
    ]

    # 골반 - 무릎의 직선 기울기 찾기
    waist_to_knee_slope = util.find_straightslope(waist[0], waist[1], knee[0], knee[1])

    # 골반 - 무릎 - 발목 각도 찾기
    between_degree = util.calculate_angle(waist, knee, ankle)

    # 최종 자세판단
    if np.abs(waist_to_knee_slope) < 5:
        if 50 < between_degree < 90:
            print("1-2: 가동범위 굿")
            return True
        else:
            return False
    elif np.abs(waist_to_knee_slope) > 5 and np.abs(waist_to_knee_slope) < 50:
        return False
    else:
        return False

def checkKneeposition(data):
    # 좌표 받아오기
    left_waist = data["keypoints"][11]["position"]
    right_waist = data["keypoints"][12]["position"]
    left_knee = data["keypoints"][13]["position"]
    right_knee = data["keypoints"][14]["position"]
    left_ankle = data["keypoints"][15]["position"]
    right_ankle = data["keypoints"][16]["position"]

    # 관절 좌, 우 중심점 찾기
    waist = [
        (left_waist["x"] + right_waist["x"]) / 2,
        (left_waist["y"] + right_waist["y"]) / 2,
    ]
    knee = [
        (left_knee["x"] + right_knee["x"]) / 2,
        (left_knee["y"] + right_knee["y"]) / 2,
    ]
    ankle = [
        (left_ankle["x"] + right_ankle["x"]) / 2,
        (left_ankle["y"] + right_ankle["y"]) / 2,
    ]

    # 골반 - 무릎의 직선 기울기 / 각도 찾기
    waist_to_knee_slope = util.find_straightslope(waist[0], waist[1], knee[0], knee[1])

    if waist_to_knee_slope > 0:
        waist_to_knee_degree = util.calculate_angle(
            [1, waist_to_knee_slope], [0, 0], [1, 0]
        )
    else:
        waist_to_knee_degree = util.calculate_angle(
            [-1, waist_to_knee_slope], [0, 0], [-1, 0]
        )

    # 무릎 - 발목의 직선 기울기 / 각도 찾기
    knee_to_ankle_slope = util.find_straightslope(knee[0], knee[1], ankle[0], ankle[1])

    if knee_to_ankle_slope > 0:
        knee_to_ankle_degree = util.calculate_angle(
            [1, knee_to_ankle_slope], [0, 0], [1, 0]
        )
    else:
        knee_to_ankle_degree = util.calculate_angle(
            [-1, knee_to_ankle_slope], [0, 0], [-1, 0]
        )

    # 최종 판단
    if waist_to_knee_degree < 10 and knee_to_ankle_degree > 45:
        print("2-1: 무릎이 적당하게 나감")
        return True
    else:
        return False

def checkCenterofgravity(data):
    # 좌표 받아오기
    left_shoulder = data["keypoints"][5]["position"]
    right_shoulder = data["keypoints"][6]["position"]
    left_knee = data["keypoints"][13]["position"]
    right_knee = data["keypoints"][14]["position"]
    left_ankle = data["keypoints"][15]["position"]
    right_ankle = data["keypoints"][16]["position"]

    # 관절 좌, 우 중심점 찾기
    shoulder = [
        (left_shoulder["x"] + right_shoulder["x"]) / 2,
        (left_shoulder["y"] + right_shoulder["y"]) / 2,
    ]
    knee = [
        (left_knee["x"] + right_knee["x"]) / 2,
        (left_knee["y"] + right_knee["y"]) / 2,
    ]
    ankle = [
        (left_ankle["x"] + right_ankle["x"]) / 2,
        (left_ankle["y"] + right_ankle["y"]) / 2,
    ]

    # 어깨가 무릎보다 과도하게 앞으로 나오면 무게중심이 너무 앞으로 쏠린 경우임
    if np.abs(shoulder[0] - knee[0]) > 50:
        return False

    # 어깨와 발목이 비슷한 좌표 포인트에서 움직이는지 판단!
    diff = np.abs(shoulder[0] - ankle[0])
    if diff < 50:
        print("2-2: 무게중심 적절함")
        return True
    else:
        return False


def checkbackline(data, image):
    # 관절 좌표 처리
    left_shoulder = data["keypoints"][5]["position"]
    right_shoulder = data["keypoints"][6]["position"]
    left_waist = data["keypoints"][11]["position"]
    right_waist = data["keypoints"][12]["position"]

    # 관절 좌, 우 중심점 찾기
    shoulder = [
        (left_shoulder["x"] + right_shoulder["x"]) / 2,
        (left_shoulder["y"] + right_shoulder["y"]) / 2,
    ]
    waist = [
        (left_waist["x"] + right_waist["x"]) / 2,
        (left_waist["y"] + right_waist["y"]) / 2,
    ]

    # 이미지와 관절 좌표 이용하여, 등 경계선과의 거리 측정하기
    slope = util.find_straightslope(shoulder[0], shoulder[1], waist[0], waist[1])
    if shoulder[0] < waist[0]:
        distance = util.find_distancefromboarderline(
            image, slope, int(shoulder[0]), int(shoulder[1]), int(waist[0])
        )
    else:
        distance = util.find_distancefromboarderline(
            image, slope, int(waist[0]), int(waist[1]), int(shoulder[0])
        )

    print("거리의 최대 차이 : ", max(distance), min(distance))
    diff = max(distance) - min(distance)
    if diff > 20:
        return False
    else:
        return True


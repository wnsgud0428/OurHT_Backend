import numpy as np


"""
0: nose
1: left_eye
2: right_eye
3: left_ear
4: right_ear
5: left_shoulder
6: right_shoulder
7: left_elbow
8: right_elbow
9: left_wrist
10: right_wrist
11: left_hip
12: right_hip
13: left_knee
14: right_knee
15: left_ankle
16: right_ankle
"""

# 각도 계산 하는 함수 a-b-c의 각도
"""
b----a
 `
  `
   `c
"""


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def isUpperbodyNotBent(request):
    is_upperbody_not_bent = False

    left_shoulder_x = request.data["keypoints"][5]["position"]["x"]
    left_shoulder_y = request.data["keypoints"][5]["position"]["y"]

    left_hip_x = request.data["keypoints"][11]["position"]["x"]
    left_hip_y = request.data["keypoints"][11]["position"]["y"]

    left_knee_x = request.data["keypoints"][13]["position"]["x"]
    left_knee_y = request.data["keypoints"][13]["position"]["y"]

    left_ankle_x = request.data["keypoints"][15]["position"]["x"]
    left_ankle_y = request.data["keypoints"][15]["position"]["y"]

    left_shoulder = [left_shoulder_x, left_shoulder_y]
    left_hip = [left_hip_x, left_hip_y]
    left_knee = [left_knee_x, left_knee_y]
    left_ankle = [left_ankle_x, left_ankle_y]

    shoulder_hip_knee_angle = calculate_angle(left_shoulder, left_hip, left_knee)
    hip_knee_ankle_angle = calculate_angle(left_hip, left_knee, left_ankle)

    ### 발목의 중앙 정렬을 위해 --> 정확도 향상을 하려면 left_ankle뿐만 아니라 right_ankle도 고려해야됨
    print(f"어깨-엉덩이-무릎 각도:{shoulder_hip_knee_angle}")
    print(f"엉덩이-무릎-발목 각도:{hip_knee_ankle_angle}")

    if 45 < shoulder_hip_knee_angle < 180:
        is_upperbody_not_bent = True
        print("적당하게 숙인 각도에요")
    elif shoulder_hip_knee_angle <= 45:
        is_upperbody_not_bent = False
        print("너무 굽었어요!")
    elif shoulder_hip_knee_angle > 180:
        is_upperbody_not_bent = None
        print("몸을 뒤로 제끼면 안되죠!")

    if is_upperbody_not_bent == True:
        return True
    else:
        return False


# 눈-귀-어깨 각도 비교
def isFaceForward(request):
    is_face_forward = False

    left_eye_x = request.data["keypoints"][1]["position"]["x"]
    left_eye_y = request.data["keypoints"][1]["position"]["y"]

    left_ear_x = request.data["keypoints"][3]["position"]["x"]
    left_ear_y = request.data["keypoints"][3]["position"]["y"]

    left_shoulder_x = request.data["keypoints"][5]["position"]["x"]
    left_shoulder_y = request.data["keypoints"][5]["position"]["y"]

    left_eye = [left_eye_x, left_eye_y]
    left_ear = [left_ear_x, left_ear_y]
    left_shoulder = [left_shoulder_x, left_shoulder_y]

    eye_ear_shoulder_angle = calculate_angle(left_eye, left_ear, left_shoulder)

    ###스쿼트시 고개를 잘 유지하는지
    print(f"눈-귀-어깨 각도:{eye_ear_shoulder_angle}")

    if 70 < eye_ear_shoulder_angle < 90:
        is_face_forward = True
        print("적당히 고개를 들었어요")
    elif eye_ear_shoulder_angle >= 90:
        is_face_forward = False
        print("고개를 너무 들었어요!")
    elif eye_ear_shoulder_angle <= 70:
        is_face_forward = None
        print("고개를 너무 숙였어요!")

    if is_face_forward == True:
        return True
    else:
        return False

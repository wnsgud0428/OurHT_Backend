import util, numpy as np, cv2

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
    '''
    if np.abs(waist_to_knee_slope) < 5:
        if between_degree > 50 and between_degree < 90:
            print("1-2: 가동범위 굿")
            return 3
        else:
            return 2
    elif np.abs(waist_to_knee_slope) > 5 and np.abs(waist_to_knee_slope) < 50:
        return 2
    else:
        return 1
        '''
    if np.abs(waist_to_knee_slope) < 5:
        if between_degree > 50 and between_degree < 90:
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
    left_waist = data["keypoints"][11]["position"]
    right_waist = data["keypoints"][12]["position"]
    left_knee = data["keypoints"][13]["position"]
    right_knee = data["keypoints"][14]["position"]
    left_ankle = data["keypoints"][15]["position"]
    right_ankle = data["keypoints"][16]["position"]

    # 관절 좌, 우 중심점 찾기
    shoulder = [
        (left_shoulder["x"] + right_shoulder["x"]) / 2,
        (left_shoulder["y"] + right_shoulder["y"]) / 2,
    ]
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

    # 어깨가 무릎보다 앞으로 나오면 무게중심이 너무 앞으로 쏠린 경우임
    if waist[0] > knee[0]:  # 왼쪽을 보며 스쿼트하는 경우
        if shoulder[0] < knee[0]:
            return False
    else:  # 오른쪽을 보며 스쿼트하는 경우
        if shoulder[0] > knee[0]:
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
        distance = util.find_distancefromboarderline(image, slope, int(shoulder[0]), int(shoulder[1]), int(waist[0]))
    else:
        distance = util.find_distancefromboarderline(image, slope, int(waist[0]), int(waist[1]), int(shoulder[0]))

    print("거리의 최대 차이 : ", max(distance), min(distance))
    diff = max(distance) - min(distance)
    if diff > 50:
        return False
    else:
        return True

    # 2. 곡률 데이터를 통해 굽었는지 판정하기 - 곡률이 제대로 측정되지 않아서 보류

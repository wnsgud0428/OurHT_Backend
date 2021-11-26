from util import calculate_angle


def returnSquatState(data):
    # 좌표 받아오기
    left_hip = data["keypoints"][11]["position"]
    right_hip = data["keypoints"][12]["position"]
    left_knee = data["keypoints"][13]["position"]
    right_knee = data["keypoints"][14]["position"]

    # 관절 좌, 우 중심점 찾기
    hip = [
        (left_hip["x"] + right_hip["x"]) / 2,
        (left_hip["y"] + right_hip["y"]) / 2,
    ]
    knee = [
        (left_knee["x"] + right_knee["x"]) / 2,
        (left_knee["y"] + right_knee["y"]) / 2,
    ]

    # extra_point=[hip의 x, knee의 y]
    # 즉, hip에서 수직으로 선 긋고, knee에서 수평으로 선 그엇을때 만나는 점
    extra_point = [hip[0], knee[1]]

    angle = calculate_angle(hip, knee, extra_point)

    if hip[1] < knee[1]:  # 일반적인 경우 --> hip의 y좌표가 작다.
        if angle < 40:  # 덜 앉았을 경우에도 스쿼트로 인식하게 만들기
            print("squat")
            return "squat"
        elif angle > 80:
            print("stand")
            return "stand"
        else:
            print("ongoing")
            return "ongoing"
    else:  # 가동범위가 좋아서, 깊게 앉은 경우 --> hip의 y좌표가 더 커진다.
        print("squat")
        return "squat"

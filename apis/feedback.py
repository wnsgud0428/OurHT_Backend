import numpy, cv2
from scipy.interpolate import splprep, splev
import base64

import util


def isUpperbodyNotTooForward(data):
    is_upperbody_not_bent = False

    left_shoulder_x = data["keypoints"][5]["position"]["x"]
    left_shoulder_y = data["keypoints"][5]["position"]["y"]

    left_hip_x = data["keypoints"][11]["position"]["x"]
    left_hip_y = data["keypoints"][11]["position"]["y"]

    left_shoulder = [
        left_shoulder_x,
        left_shoulder_y,
    ]
    left_hip = [left_hip_x, left_hip_y]
    extra_point = [left_shoulder_x, left_hip_y]

    shoulder_hip_extra_angle = util.calculate_angle(
        left_shoulder, left_hip, extra_point
    )
    print("[1](상체 숙여짐)shoulder_hip_extra_angle: ", shoulder_hip_extra_angle)

    if shoulder_hip_extra_angle < 40:  # 0에 가까워질수록 지면과 수평(안 좋아짐)
        is_upperbody_not_bent = False
        print("[1]X")
    else:
        is_upperbody_not_bent = True
        print("[1]O")

    if is_upperbody_not_bent == True:
        return True
    else:
        return False


def isFaceForward(data):
    is_face_forward = False

    left_eye_x = data["keypoints"][1]["position"]["x"]
    left_eye_y = data["keypoints"][1]["position"]["y"]

    left_ear_x = data["keypoints"][3]["position"]["x"]
    left_ear_y = data["keypoints"][3]["position"]["y"]

    left_eye = [left_eye_x, left_eye_y]
    left_ear = [left_ear_x, left_ear_y]
    extra_point = [left_ear_x, left_eye_y]

    ear_eye_extra_angle = util.calculate_angle(left_ear, left_eye, extra_point)

    print("[2](고개) ear_eye_extra_angle: ", ear_eye_extra_angle)
    if ear_eye_extra_angle > 40:  # 값이 90에 가까워 질수록 땅을 바라봄(안좋은 자세 됨)
        is_face_forward = False
        print("[2]X")
    else:
        is_face_forward = True
        print("[2]O")

    if is_face_forward == True:
        return True
    else:
        return False


def isRangeGood(data):
    # 좌표 받아오기
    left_hip_x = data["keypoints"][11]["position"]["x"]
    left_hip_y = data["keypoints"][11]["position"]["y"]
    left_knee_x = data["keypoints"][13]["position"]["x"]
    left_knee_y = data["keypoints"][13]["position"]["y"]

    # 관절 좌, 우 중심점 찾기
    left_hip = [left_hip_x, left_hip_y]
    left_knee = [left_knee_x, left_knee_y]
    extra_point = [left_hip_x, left_knee_y]

    hip_knee_extra_angle = util.calculate_angle(left_hip, left_knee, extra_point)

    print("[3](가동범위) hip_knee_extra_angle: ", hip_knee_extra_angle)
    if left_hip_y > left_knee_y:
        print("[3]O")
        return True
    else:
        if hip_knee_extra_angle < 20:  # 덜 앉았을 경우에도 스쿼트로 인식하게 만들기
            print("[3]△")
            return True
        else:
            print("[3]X")
            return False


def isKneePositionGood(data):
    left_knee_x = data["keypoints"][13]["position"]["x"]
    left_knee_y = data["keypoints"][13]["position"]["y"]

    left_ankle_x = data["keypoints"][15]["position"]["x"]
    left_ankle_y = data["keypoints"][15]["position"]["y"]

    left_knee = [left_knee_x, left_knee_y]
    left_ankle = [left_ankle_x, left_ankle_y]
    extra_point = [left_knee_x, left_ankle_y]

    knee_ankle_extra_angle = util.calculate_angle(left_knee, left_ankle, extra_point)

    print("[4](무릎 튀어나옴) knee_ankle_extra_angle: ", knee_ankle_extra_angle)
    if knee_ankle_extra_angle < 50:
        print("[4]X")
        return False
    else:
        print("[4]O")
        return True


def isCenterOfGravityProper(data):
    # 좌표 받아오기
    left_shoulder_x = data["keypoints"][5]["position"]["x"]
    left_shoulder_y = data["keypoints"][5]["position"]["y"]

    left_ankle_x = data["keypoints"][15]["position"]["x"]
    left_ankle_y = data["keypoints"][15]["position"]["y"]

    left_shoulder = [left_shoulder_x, left_shoulder_y]
    left_ankle = [left_ankle_x, left_ankle_y]
    extra_point = [left_shoulder_x, left_ankle_y]

    shoulder_ankle_extra_angle = util.calculate_angle(
        left_shoulder, left_ankle, extra_point
    )

    print("[5](무게중심) shoulder_ankle_extra_angle: ", shoulder_ankle_extra_angle)

    # 최종 판단
    if shoulder_ankle_extra_angle < 70:
        print("[5]X")
        return False
    else:
        print("[5]O")
        return True


def returnLineEquCoef(p1, p2):
    """[기울기m, y절편] 리턴"""
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    if x2 != x1:
        m = (y2 - y1) / (x2 - x1)  # 기울기 m 계산(a값)
        n = y1 - (m * x1)  # y 절편 계산(b값)
    else:
        m = 100
        n = y1 - (m * x1)
    return [m, n]


def isPointUnderTheLine(line_equ_coef, point):
    """점이 직선의 밑에있는지 따져 T/F 리턴"""
    m = line_equ_coef[0]
    n = line_equ_coef[1]
    x1 = point[0]
    y1 = point[1]
    result = m * x1 + n - y1
    if result > 0:
        return True
    else:
        return False


def newCheckBackLine(data, image):  # 파라미터에 있는 image는 remove bg 처리가 되어있음
    """등 분석해서, 굽음 여부 따져 T/F 리턴"""
    # origin_image = cv2.resize(image, dsize=(640, 480), interpolation=cv2.INTER_AREA)
    # removebg를 이용하면 size가 이상해져서 다시 640x480으로 resize
    image = cv2.resize(image, dsize=(640, 480), interpolation=cv2.INTER_AREA)

    # json으로 받아진 관절포인트에서 origin_left_shoulder 뽑아냄
    # origin_left_shoulder = list(
    #     map(
    #         int,
    #         [
    #             data["keypoints"][5]["position"]["x"],
    #             data["keypoints"][5]["position"]["y"],
    #         ],
    #     )
    # )
    # origin_left_hip = list(
    #     map(
    #         int,
    #         [
    #             data["keypoints"][11]["position"]["x"],
    #             data["keypoints"][11]["position"]["y"],
    #         ],
    #     )
    # )

    origin_left_shoulder = list(map(int, [data[0], data[1]]))
    origin_left_hip = list(map(int, [data[2], data[3]]))

    # 앞에서의 어깨, 골반 포인트를 이용해 1차 ROI 설정
    roi = {
        "x_begin": origin_left_shoulder[0],
        "x_end": 640,
        "y_begin": 0,
        "y_end": origin_left_hip[1],
    }
    image = image[roi["y_begin"] : roi["y_end"], roi["x_begin"] : roi["x_end"]]

    # slice한 이미지의 관절 포인트 값 수정
    left_shoulder = [origin_left_shoulder[0], origin_left_shoulder[1]]
    left_hip = [origin_left_hip[0], origin_left_hip[1]]

    left_shoulder[0] -= origin_left_shoulder[0]
    left_shoulder[1] -= 0
    left_hip[0] -= origin_left_shoulder[0]
    left_hip[1] -= 0

    # contour 그리기
    image1_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    contours, hierarcy = cv2.findContours(
        image1_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    output_image = cv2.drawContours(
        image, contours, -1, (0, 255, 0), 2
    )  # 이 output_image는 contours만 그려져있음

    # ###WIP: 처음 그려진 contour에 대해서, 어깨-골반 직선 활용한 roi설정 작업중
    # list_of_contour = []
    # print(contours[0][1][0])
    # for i in range(len(contours[0])):
    #     list_of_contour.append([contours[0][i][0][0], contours[0][i][0][1]])
    # print(list_of_contour)

    # 등의 곡선을 조금더 유연하게 만들기 --> 각이 있는 다각형으로 만들기
    smoothened = []
    for contour in contours:
        x, y = contour.T
        # Convert from numpy arrays to normal arrays
        x = x.tolist()[0]
        y = y.tolist()[0]
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.splprep.html
        tck, u = splprep([x, y], u=None, s=1.0, per=1)
        # https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.linspace.html
        u_new = numpy.linspace(u.min(), u.max(), 30)
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.splev.html
        x_new, y_new = splev(u_new, tck, der=0)
        # Convert it back to numpy format for opencv to be able to display it
        res_array = [[[int(i[0]), int(i[1])]] for i in zip(x_new, y_new)]
        smoothened.append(numpy.asarray(res_array, dtype=numpy.int32))
    cv2.drawContours(image, smoothened, -1, (255, 255, 255), 2)
    # print("smoothened[0]:", type(smoothened[0]), smoothened[0])

    # interpolate된 contour 흰색으로 표시
    cv2.line(
        image,
        left_shoulder,
        left_hip,
        (255, 255, 255),
        thickness=None,
        lineType=None,
        shift=None,
    )

    # 어깨-골반 잇는 직선에 대한 방정식 구함
    line_equ_coef = returnLineEquCoef(left_shoulder, left_hip)

    # ROI 재설정 -> want_point_list에 등의 포인트 담음
    want_point_list = []
    for i in range(len(smoothened)):
        for j in range(len(smoothened[i])):
            point = [smoothened[i][j][0][0], smoothened[i][j][0][1]]

            if point[0] > left_shoulder[0] and point[1] < left_hip[1]:
                if isPointUnderTheLine(line_equ_coef, point):
                    want_point_list.append(point)
    # print(want_point_list)

    # 예외처리
    if not want_point_list:
        return False, None

    # want_point_list의 포인트들 정리
    want_point_list = list(set(map(tuple, want_point_list)))  # 중복제거..
    want_point_list = list(map(list, want_point_list))  # 중복제거..
    want_point_list.sort(key=lambda x: x[0])  # x좌표에 대해 오름차순으로 정렬

    ### 굽은거 측정을 잘 못해냄
    # want_to_remove = []
    # for i in range(len(want_point_list)):
    #     if want_point_list[i][1] <= left_shoulder[1]:
    #         want_to_remove.append(i)
    # want_to_remove.reverse()
    # for i in want_to_remove:
    #     want_point_list.pop(i)

    ### 여러번 테스트해서 앞뒤 포인트들 얼마나 짤라낼지 정해야됨.
    ### !!!!!!!! 그날 컨디션에 따라 값날리는 거 달라야됨.
    # 앞에꺼 날리기
    want_point_list.pop(0)
    want_point_list.pop(0)
    want_point_list.pop(0)

    # 뒤에꺼 날리기
    want_point_list.pop()
    want_point_list.pop()
    print("want_point_list:", want_point_list)
    # print("필터링된 want_point_list:", want_point_list)

    # # 파란색으로 등 라인 그리기
    # for i in range(num_of_check_point - 1):
    #     cv2.line(
    #         image,
    #         want_point_list[i],
    #         want_point_list[i + 1],
    #         (255, 0, 0),
    #         thickness=3,
    #         lineType=None,
    #         shift=None,
    #     )

    num_of_check_point = len(want_point_list)
    for i in range(num_of_check_point):
        # 파란색으로 등에있는 점 찍기
        cv2.line(
            image,
            want_point_list[i],
            want_point_list[i],
            (255, 0, 0),
            thickness=3,
            lineType=None,
            shift=None,
        )

    # ###기존의 back_point_slope와 shoulder_to_hip_slope의 차이를 sum해서 측정하는 방식
    # ###문제가 좀 있는듯
    # for i in range(num_of_check_point) - 1:
    #     coef = returnLineEquCoef(want_point_list[i], want_point_list[i + 1])
    #     back_point_slope = coef[0]
    #     slope_diff = abs(shoulder_to_hip_slope - back_point_slope)
    #     print(slope_diff)
    #     slope_diff_sum += slope_diff
    # print("slope_diff_sum:", slope_diff_sum)

    # ###기울기의 변화량을 이용하여 측정
    # ###문제 있음
    # slope_diff_of_neighbor_line_sum = 0
    # for i in range(num_of_check_point - 2):
    #     coef1 = returnLineEquCoef(want_point_list[i], want_point_list[i + 1])
    #     coef2 = returnLineEquCoef(want_point_list[i + 1], want_point_list[i + 2])

    #     slope_diff_of_neighbor_line = abs(coef2[0] - coef1[0])
    #     print(slope_diff_of_neighbor_line)
    #     slope_diff_of_neighbor_line_sum += slope_diff_of_neighbor_line
    # print("slope_diff_of_neighbor_line_sum:", slope_diff_of_neighbor_line_sum)

    ###첫부분의 기울기와 끝부분의 기울기의 차이 이용
    coef1 = returnLineEquCoef(want_point_list[0], want_point_list[1])
    coef2 = returnLineEquCoef(
        want_point_list[num_of_check_point - 2], want_point_list[num_of_check_point - 1]
    )
    shoulder_part_slope = coef1[0]
    hip_part_slope = coef2[0]
    print("shoulder_part_slope:", shoulder_part_slope)
    print("hip_part_slope:", hip_part_slope)
    hip_shoulder_slope_diff = abs(hip_part_slope - shoulder_part_slope)
    print("어깨쪽 기울기와 골반쪽 기울기의 차이: ", hip_shoulder_slope_diff)

    ###새로운 접근 -> 각도 이용
    ##준비물: 아래 주석
    # want_point_list[0], want_point_list[1]
    # want_point_list[num_of_check_point - 2], want_point_list[num_of_check_point - 1]
    x_move = want_point_list[num_of_check_point - 2][0] - want_point_list[1][0]
    y_move = want_point_list[num_of_check_point - 2][1] - want_point_list[1][1]
    moved_point = [want_point_list[0][0] + x_move, want_point_list[0][1] + y_move]
    angle_for_slope_diff = util.calculate_angle(
        moved_point,
        want_point_list[num_of_check_point - 2],
        want_point_list[num_of_check_point - 1],
    )
    print("angle_for_slope_diff: ", angle_for_slope_diff)

    # interpolated contour, 등 포인트 모두 그려진 이미지 base64코드로 저장
    _, im_arr = cv2.imencode(".jpg", output_image)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    im_b64 = str(im_b64)
    im_b64 = im_b64[2:]
    im_b64 = im_b64[:-1]
    # print(im_b64)
    back_image_base64 = im_b64

    # 윈도우 창 띄어서 처리된 이미지 보기
    # cv2.imshow("output_image", output_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # if hip_shoulder_slope_diff < 0.5: # 기울기이용
    if angle_for_slope_diff > 165:
        # print("좋은 허리")
        return True, back_image_base64
    else:
        # print("굽은 허리")
        return False, back_image_base64


###### 아래는 테스트 용
image_input_type = "test_junhyeong"  ###이거를 good, wrong으로 바꿔가야 demo해보면 됨
if image_input_type == "wrong":
    image = cv2.imread("test_images/resize_" + image_input_type + "2.jpg_removebg.png")
    data = {
        "score": 0.8330827811185051,
        "keypoints": [
            {
                "score": 0.9836747646331787,
                "part": "nose",
                "position": {"x": 262.58542071984436, "y": 111.90823727938795},
            },
            {
                "score": 0.9730626940727234,
                "part": "leftEye",
                "position": {"x": 255.6393254499027, "y": 93.0498824836059},
            },
            {
                "score": 0.5370296239852905,
                "part": "rightEye",
                "position": {"x": 251.15386369163426, "y": 100.73956267203691},
            },
            {
                "score": 0.9943153262138367,
                "part": "leftEar",
                "position": {"x": 293.55839235773345, "y": 66.10110742440496},
            },
            {
                "score": 0.33212506771087646,
                "part": "rightEar",
                "position": {"x": 667.2448017996109, "y": 81.8815399328044},
            },
            {
                "score": 0.9887490272521973,
                "part": "leftShoulder",
                "position": {"x": 347.4719190783074, "y": 100.01493938228627},
            },
            {
                "score": 0.8504123687744141,
                "part": "rightShoulder",
                "position": {"x": 360.6937393604086, "y": 90.64218787949319},
            },
            {
                "score": 0.9700634479522705,
                "part": "leftElbow",
                "position": {"x": 268.9705625303988, "y": 163.04253612775258},
            },
            {
                "score": 0.6045985817909241,
                "part": "rightElbow",
                "position": {"x": 268.6564855909533, "y": 194.49576738584844},
            },
            {
                "score": 0.9927899837493896,
                "part": "leftWrist",
                "position": {"x": 165.80140822592412, "y": 196.8807872712921},
            },
            {
                "score": 0.6922425031661987,
                "part": "rightWrist",
                "position": {"x": 197.9435949659533, "y": 219.73616367794688},
            },
            {
                "score": 0.9769037365913391,
                "part": "leftHip",
                "position": {"x": 512.3182909776265, "y": 263.33344296470204},
            },
            {
                "score": 0.9119596481323242,
                "part": "rightHip",
                "position": {"x": 491.11434520914395, "y": 258.41208028052137},
            },
            {
                "score": 0.9922526478767395,
                "part": "leftKnee",
                "position": {"x": 344.0522783925097, "y": 282.4971664507772},
            },
            {
                "score": 0.8926414847373962,
                "part": "rightKnee",
                "position": {"x": 332.7205815296693, "y": 266.7994302542098},
            },
            {
                "score": 0.9467653632164001,
                "part": "leftAnkle",
                "position": {"x": 408.2204903331712, "y": 478.2800609213083},
            },
            {
                "score": 0.5228210091590881,
                "part": "rightAnkle",
                "position": {"x": 422.71301982003894, "y": 483.8098460775583},
            },
        ],
    }
elif image_input_type == "good":
    image = cv2.imread("test_images/resize_" + image_input_type + "2.jpg_removebg.png")
    data = {
        "score": 0.8125545137068805,
        "keypoints": [
            {
                "score": 0.9635857939720154,
                "part": "nose",
                "position": {"x": 272.6152305751459, "y": 89.09702439382286},
            },
            {
                "score": 0.9748300909996033,
                "part": "leftEye",
                "position": {"x": 275.6293888314689, "y": 76.85652342485022},
            },
            {
                "score": 0.2157295197248459,
                "part": "rightEye",
                "position": {"x": 650.9804383511673, "y": 75.96101909103788},
            },
            {
                "score": 0.978201687335968,
                "part": "leftEar",
                "position": {"x": 306.2430842655642, "y": 64.31639360022669},
            },
            {
                "score": 0.16974280774593353,
                "part": "rightEar",
                "position": {"x": 634.8241807514592, "y": 80.27110361682318},
            },
            {
                "score": 0.9955292344093323,
                "part": "leftShoulder",
                "position": {"x": 361.6723537816148, "y": 106.42494004007447},
            },
            {
                "score": 0.9652485251426697,
                "part": "rightShoulder",
                "position": {"x": 329.67853234435796, "y": 122.94076870142487},
            },
            {
                "score": 0.9809345602989197,
                "part": "leftElbow",
                "position": {"x": 274.24732490272373, "y": 163.98650648680376},
            },
            {
                "score": 0.8193921446800232,
                "part": "rightElbow",
                "position": {"x": 258.35397920719845, "y": 188.59024601279145},
            },
            {
                "score": 0.9905636310577393,
                "part": "leftWrist",
                "position": {"x": 185.53840132538912, "y": 173.6170192580149},
            },
            {
                "score": 0.7813771963119507,
                "part": "rightWrist",
                "position": {"x": 192.9134811223249, "y": 185.1835545357027},
            },
            {
                "score": 0.970457136631012,
                "part": "leftHip",
                "position": {"x": 464.4813199173152, "y": 280.2666382468426},
            },
            {
                "score": 0.9503396153450012,
                "part": "rightHip",
                "position": {"x": 477.8229116001946, "y": 286.12068136738986},
            },
            {
                "score": 0.9968057870864868,
                "part": "leftKnee",
                "position": {"x": 318.6159031493191, "y": 303.0393420599903},
            },
            {
                "score": 0.42014309763908386,
                "part": "rightKnee",
                "position": {"x": 341.81382234922177, "y": 324.1012715552137},
            },
            {
                "score": 0.9622737765312195,
                "part": "leftAnkle",
                "position": {"x": 395.3991746716926, "y": 468.26181994818654},
            },
            {
                "score": 0.6782721281051636,
                "part": "rightAnkle",
                "position": {"x": 435.507546510214, "y": 444.4550730650907},
            },
        ],
    }
else:
    if image_input_type == "test_junhyeong":
        image = cv2.imread("test_images/no-bg.png")
        data = {
            "score": 0.8743049355552477,
            "keypoints": [
                {
                    "score": 0.9872514009475708,
                    "part": "nose",
                    "position": {"x": 182.56446452456225, "y": 197.27179808937822},
                },
                {
                    "score": 0.9854617118835449,
                    "part": "leftEye",
                    "position": {"x": 184.10999817607004, "y": 184.96126639410622},
                },
                {
                    "score": 0.4244021773338318,
                    "part": "rightEye",
                    "position": {"x": 177.24789868069067, "y": 184.01433598809908},
                },
                {
                    "score": 0.9961262941360474,
                    "part": "leftEar",
                    "position": {"x": 212.83945996473736, "y": 172.44899611398964},
                },
                {
                    "score": 0.048550475388765335,
                    "part": "rightEar",
                    "position": {"x": 188.52637858706225, "y": 186.98309231298575},
                },
                {
                    "score": 0.9994828701019287,
                    "part": "leftShoulder",
                    "position": {"x": 256.8241959508755, "y": 209.4127532484618},
                },
                {
                    "score": 0.9895740151405334,
                    "part": "rightShoulder",
                    "position": {"x": 228.71502234314204, "y": 215.72418054768457},
                },
                {
                    "score": 0.99922776222229,
                    "part": "leftElbow",
                    "position": {"x": 253.15256794139106, "y": 271.13001690009713},
                },
                {
                    "score": 0.7465185523033142,
                    "part": "rightElbow",
                    "position": {"x": 216.94558228964007, "y": 253.84051545296307},
                },
                {
                    "score": 0.9970807433128357,
                    "part": "leftWrist",
                    "position": {"x": 177.49188731152725, "y": 267.01752499595204},
                },
                {
                    "score": 0.8548148274421692,
                    "part": "rightWrist",
                    "position": {"x": 177.42941771035993, "y": 259.2761862957416},
                },
                {
                    "score": 0.9964235424995422,
                    "part": "leftHip",
                    "position": {"x": 336.4056800218872, "y": 333.7291278740285},
                },
                {
                    "score": 0.9797573685646057,
                    "part": "rightHip",
                    "position": {"x": 304.1603652419747, "y": 329.5813431023316},
                },
                {
                    "score": 0.9982239603996277,
                    "part": "leftKnee",
                    "position": {"x": 234.82931055447472, "y": 321.737560212921},
                },
                {
                    "score": 0.9412000179290771,
                    "part": "rightKnee",
                    "position": {"x": 230.1957874817607, "y": 361.4257559504534},
                },
                {
                    "score": 0.9969828724861145,
                    "part": "leftAnkle",
                    "position": {"x": 293.0812636794747, "y": 431.44919598040804},
                },
                {
                    "score": 0.9221053123474121,
                    "part": "rightAnkle",
                    "position": {"x": 261.4917847154669, "y": 430.4498006395725},
                },
            ],
        }
    if image_input_type == "test_woman_cat":
        image = cv2.imread("test_images/flip_resize_woman_cat.png")
        data = {
            "score": 0.7363666725509307,
            "keypoints": [
                {
                    "score": 0.8380802273750305,
                    "part": "nose",
                    "position": {"x": 179.38940144698444, "y": 254.11099923089378},
                },
                {
                    "score": 0.7812063097953796,
                    "part": "leftEye",
                    "position": {"x": 165.23188609557394, "y": 230.79121802137306},
                },
                {
                    "score": 0.37397244572639465,
                    "part": "rightEye",
                    "position": {"x": 166.26151355787937, "y": 248.4626224498057},
                },
                {
                    "score": 0.9030696749687195,
                    "part": "leftEar",
                    "position": {"x": 153.7268588886187, "y": 219.59700352169688},
                },
                {
                    "score": 0.2425304800271988,
                    "part": "rightEar",
                    "position": {"x": 173.5813434764105, "y": 173.1404896474255},
                },
                {
                    "score": 0.9680370092391968,
                    "part": "leftShoulder",
                    "position": {"x": 221.16756216561285, "y": 159.55956651756802},
                },
                {
                    "score": 0.9115365147590637,
                    "part": "rightShoulder",
                    "position": {"x": 211.35590193336577, "y": 161.46543828934585},
                },
                {
                    "score": 0.9524546265602112,
                    "part": "leftElbow",
                    "position": {"x": 207.90895929596303, "y": 288.07423645968265},
                },
                {
                    "score": 0.7065163850784302,
                    "part": "rightElbow",
                    "position": {"x": 194.80377553501947, "y": 277.7810336888763},
                },
                {
                    "score": 0.9529217481613159,
                    "part": "leftWrist",
                    "position": {"x": 215.26783271522373, "y": 362.52704521534974},
                },
                {
                    "score": 0.46546468138694763,
                    "part": "rightWrist",
                    "position": {"x": 169.4955693701362, "y": 337.1966331363342},
                },
                {
                    "score": 0.9726027250289917,
                    "part": "leftHip",
                    "position": {"x": 402.53404669260703, "y": 178.47902920579662},
                },
                {
                    "score": 0.8953964710235596,
                    "part": "rightHip",
                    "position": {"x": 350.03454067363816, "y": 190.68093097271696},
                },
                {
                    "score": 0.9698488116264343,
                    "part": "leftKnee",
                    "position": {"x": 396.68759119649803, "y": 385.25891556023316},
                },
                {
                    "score": 0.5270951986312866,
                    "part": "rightKnee",
                    "position": {"x": 403.1450252310311, "y": 359.03988220531085},
                },
                {
                    "score": 0.694111168384552,
                    "part": "leftAnkle",
                    "position": {"x": 219.08159426678017, "y": 370.1622965916451},
                },
                {
                    "score": 0.36338895559310913,
                    "part": "rightAnkle",
                    "position": {"x": 203.09534213886187, "y": 337.5737734779793},
                },
            ],
        }

# newCheckBackLine(data, image)

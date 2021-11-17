# 잡다하게 필요한 것 같은 함수들
# 모두 수학적인 좌표 기준으로 작성
# 함수에 매개변수 넣을 때, 수학적인 좌표 기준으로 넣어야함!

import numpy as np
import math, cv2

# 임의의 두 점이 주어질 때, 직선의 기울기 찾기
def find_straightslope(first_x, first_y, second_x, second_y):

    # 기울기 구하기
    # 기울기 0과 무한대인경우 예외처리
    if first_x == second_x:
        slope = 9999999
    elif first_y == second_y:
        slope = -9999999
    else:
        slope = (second_y - first_y) / (second_x - first_x)
    return slope

# 점과 직선사이 거리 찾기
def find_distancefromline(slope, line_x, line_y, point_x, point_y):

    # 기울기 0과 무한대인경우 예외처리
    if slope == 9999999:
        return abs(point_x - line_x)
    elif slope == -9999999:
        return abs(point_y - line_y)

    # 연립방정식 두개 풀기
    left_side = np.array([[slope, -1], [-1/slope, -1]])
    right_side = np.array([slope * line_x - line_y, (-1/slope) * point_x - point_y])
    result = np.linalg.solve(left_side, right_side)

    # 교점과 주어진 점 거리 구하기
    dist_x, dist_y = pow(result[0] - point_x, 2), pow(result[1] - point_y, 2)
    answer = math.sqrt(dist_x + dist_y)
    
    return answer

# print(find_distancefromline())

# 한 직선이 주어지고, 그 직선에 수직인 직선을 따라가면서 그림의 경계점까지의 거리 찾기
# start_x < end_x 여야함!
def find_distancefromboarderline(picture, slope, start_x, start_y, end_x):
    # 그림의 가로, 세로 크기
    len_y = picture.shape[0]  # 세로
    len_x = picture.shape[1]  # 가로

    # 결과 길이, 좌표를 담은 배열
    distance_result, coor_result = [], []

    # 주어진 직선 정의
    basic_line = [slope, (-slope * start_x) + start_y]

    slope_step = 1
    for i in range(start_x, end_x, slope_step):
        new_x, new_y = i, (basic_line[0] * i) + basic_line[1]
        new_y = int(round(new_y))
        
        # 매 Point에 대해 수직인 직선 정의
        new_slope = -1/slope
        perpen_line = [new_slope, (-new_slope * new_x) + new_y]

        if new_y < 0:
            break
        while picture[len_y - new_y][new_x][0] != 0 or picture[len_y - new_y][new_x][1] != 0 or picture[len_y - new_y][new_x][2] != 0:
            # 직선 따라가면서 경계 찾기
            if new_slope > 0:
                new_x += slope_step
            else:
                new_x -= slope_step
            new_y = int(round((perpen_line[0] * new_x) + perpen_line[1]))
            if (new_x >= len_x) or (new_x < 0) or (new_y >= len_y) or (new_y < 0):
                break

        distance_result.append(math.sqrt((i - new_x) * (i - new_x) + (basic_line[0] * i + basic_line[1] - new_y) * (basic_line[0] * i + basic_line[1] - new_y)))
        coor_result.append([new_x, new_y])

    return distance_result

# 세 점이 있을 때, 각도 찾기, b가 끼인 점
def calculate_angle(a, b, c):

    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle
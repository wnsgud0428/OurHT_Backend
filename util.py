# 잡다하게 필요한 것 같은 함수들
import numpy as np
import math

# 직선의 기울기 찾기
def find_straightslope():
    # 임의로 변수 정의, 나중에 매개변수로 받아와야 함
    first_x, first_y = 0, 2
    second_x, second_y = 1, 2

    # 기울기 구하기
    # 기울기 0과 무한대인경우 예외처리
    if first_x == second_x:
        slope = 9999999
    elif first_y == second_y:
        slope = -9999999
    else:
        slope = (second_y - first_y) / (second_x - first_x)
    return slope, first_x, first_y

# 점과 직선사이 거리 찾기
def find_distancefromline():
    # 임의로 변수 정의, 나중에 매개변수로 받아와야 함
    point_x, point_y = 3, 4

    # 직선 기울기와 직선상의 한 점을 받아옴, 
    slope, line_x, line_y = find_straightslope()

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

print(find_distancefromline())
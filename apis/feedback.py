# 피드백 함수들 로직 구현 중

# 이미지는 3차원 배열로 rgb 값을 받아올 수 있음!
# ex) image[a][b] => 배열 인덱스 (a, b)부분의 [b, g, r] 값이 담겨있음! (r - g - b 순서 아님!)
#     이미지의 투명한 부분은 [0, 0, 0]으로 표현됌!
import numpy as np
import math, cv2
import util

def feedback_squrt():

    # check_head() - 목 & 머리 체크 함수
    '''
    허리 - 등 - 목으로 이어지는 직선 체크
    측면에서 귀의 좌표가 찍히는지?
    '''
    # check_back() - 등 체크 함수
    '''
    배경 제거 이미지와 응용하여 등의 굽음 측정
    '''
    # check_waist() - 허리 체크 함수
    '''
    무릎과 골반 좌표 활용해, 너무 앉거나 일어서지는 
    않았는지 체크
    '''
    # check_knee() - 무릎 체크 함수
    '''
    발목과의 좌표 비교, 굳이 발 끝이 아니여도 된다
    '''
    # check_dynamic() - 동적 정보 체크 함수
    '''
    어깨가 위 아래로만 왔다갔다 하는지
    즉, 일정하게 몸이 위아래로 움직이는지
    '''
    pass

def feedback_pushup():

    # check_head() - 목 & 머리 체크 함수
    '''
    스쿼트에서 쓰는 목 & 머리 체크 방식과 동일할 듯
    '''
    # check_back() - 등 체크 함수
    '''
    스쿼트에서 쓰는 등 체크 방식과 동일할 듯
    '''
    # check_elbow() - 팔꿈치 체크 함수
    '''
    팔꿈치의 위치가 몸통 위에서 1/3 지점(정확히 체크)
    어깨&골반&팔꿈치 좌표 활용하여 판단
    '''
    # check_lower_body() - 하반신 체크 함수
    '''
    골반 - 무릎 - 발목이 잘 이어지나 체크
    '''
    # check_dynamic() - 동적 정보 체크 함수
    '''
    좌표변화가 가장 큰 어깨 기준으로 가동범위 판단
    온 몸이 균일하게 잘 내려가고 올라오는지!
    '''
    pass

def feedback_plank():

    # check_head() - 목 & 머리 체크 함수
    '''
    스쿼트에서 쓰는 목 & 머리 체크 방식과 동일할 듯
    '''
    # check_shoulder() - 어깨 체크 함수 -> 필요한가?
    # check_elbow() - 팔꿈치 체크 함수
    '''
    푸쉬업에서 쓰는 팔꿈치 체크 방식과 동일할 듯
    '''
    # check_dynamic() - 동적 정보 체크 함수
    '''
    초기 자세를 기준으로, 
    몸의 자세가 흐트러지지 않는지 판단
    '''
    pass

# 목 - 머리 체크 함수
def check_head():
    # 어깨 위로는 어떻게 판단할지? 귀 좌표로 판단?
    pass

# 등 체크 함수
def check_back():
    ''' 등의 굽음 정도 체크 '''

    # 배경 제거된 그림 받아와야 함
    picture = []

    # 허리 좌,우 좌표를 통해 허리 중심좌표 생성
    left_waist, right_waist = [0, 0], [0, 0]
    waist = [(left_waist[0] + right_waist[0]) / 2, (left_waist[1] + right_waist[1]) / 2] 

    # 어깨 좌,우 좌표를 통해 어깨 중심좌표 생성
    left_shoulder, right_shoulder = 0, 0
    shoulder = [(left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2]

    # 허리 - 어깨를 이은 선을 토대로, 등의 윤곽선과의 거리 측정
    slope = util.find_straightslope(waist[0], waist[1], shoulder[0], shoulder[1])
    distance_arr = util.find_distancefromboarderline(picture, slope, waist[0], waist[1], shoulder[0])

    # 거리의 최댓값과 최솟값의 차
    diff = max(distance_arr) - min(distance_arr)

    ## 이제 이 정보들 가지고 어떻게 등이 안굽었는지 체크를 해야함
    ## 벗 윙크 자세도 판단
    pass

# 팔꿈치 체크 함수
def check_elbow():
    ''' 팔꿈치의 위치가 몸통 기준 어디인지? 일단 1/3 기준으로 작성 '''

    # 허리 좌,우 좌표를 통해 허리 중심좌표 생성
    left_waist, right_waist = [0, 0], [0, 0]
    waist = [(left_waist[0] + right_waist[0]) / 2, (left_waist[1] + right_waist[1]) / 2] 

    # 어깨 좌,우 좌표를 통해 어깨 중심좌표 생성
    left_shoulder, right_shoulder = 0, 0
    shoulder = [(left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2]

    # 팔꿈치 좌,우 좌표를 통해 팔꿈치 중심좌표 생성
    left_elbow, right_elbow = 0, 0
    elbow = [(left_elbow[0] + right_elbow[0]) / 2, (left_elbow[1] + right_elbow[1]) / 2]

    ## 이제 이 정보들 가지고 팔꿈치의 위치가 적절한지 판단해야 함
    pass

# 허리 체크 
def check_waist():
    pass

# 무릎 체크
def check_knee():
    pass

# 하체 체크
def check_lower_body():
    ''' 골반 - 무릎 - 발목이 일직선으로 잘 이어지는 판단 '''

    # 허리 좌,우 좌표를 통해 허리 중심좌표 생성
    left_waist, right_waist = [0, 0], [0, 0]
    waist = [(left_waist[0] + right_waist[0]) / 2, (left_waist[1] + right_waist[1]) / 2] 

    # 무릎 좌,우 좌표를 통해 무릎 중심좌표 생성
    left_knee, right_knee = [0, 0], [0, 0]
    knee = [(left_knee[0] + right_knee[0]) / 2, (left_knee[1] + right_knee[1]) / 2]

    # 발목 좌,우 좌표를 통해 무릎 중심좌표 생성
    left_ankle, right_ankle = [0, 0], [0, 0]
    ankle = [(left_ankle[0] + right_ankle[0]) / 2, (left_ankle[1] + right_ankle[1]) / 2]

    # 두 직선으로 나누어, 각각의 기울기 구함
    waist_to_knee_slope = util.find_straightslope(waist[0], waist[1], knee[0], knee[1])
    knee_to_ankle_slope = util.find_straightslope(knee[0], knee[1], ankle[0], ankle[1])

    # 골반 - 발목 총 직선 기울기
    lower_body_slope = util.find_straightslope(waist[0], waist[1], ankle[0], ankle[1])

    ## 이제 이 정보들 가지고 하체 체크
    ''' 골반과 발목 잇는 직선 기준, 무릎이 아래쪽이면 무릎이 굽혔다? '''

    pass

# 동적인 정보 활용
def check_dynamic():
    # 각 운동에서 활용해야 하는 정보들이 다르므로, 운동마다 별개로 만들어야 할듯?
    pass
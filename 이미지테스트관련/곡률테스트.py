import matplotlib.pyplot as plt
import math, cv2, numpy as np

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
    print("length :" , len_y, len_x)
    # 길이, 좌표를 담은 배열
    distance_result, coor_result = [], []

    # 주어진 직선 정의
    basic_line = [slope, (-slope * start_x) + start_y]
    print("Basic line :", basic_line)

    slope_step = 1
    for i in range(start_x, end_x, slope_step):
        new_x, new_y = i, (basic_line[0] * i) + basic_line[1]
        new_y = int(round(new_y))
        
        # 수직인 직선 정의
        new_slope = -1/slope
        perpen_line = [new_slope, (-new_slope * new_x) + new_y]
        print("Perpen line :", perpen_line)

        if new_y < 0:
            break
        while picture[len_y - new_y][new_x][0] != 0 or picture[len_y - new_y][new_x][1] != 0 or picture[len_y - new_y][new_x][2] != 0:
            # 직선 따라가면서 경계 찾기
            if new_slope > 0:
                new_x += slope_step
            else:
                new_x -= slope_step
            new_y = int(round((perpen_line[0] * new_x) + perpen_line[1]))
            #print("Dd", new_x, new_y)
            if (new_x >= len_x) or (new_x < 0) or (new_y >= len_y) or (new_y < 0):
                print("border")
                break
        print("find")
        #print(i, basic_line[0] * i + basic_line[1], new_x, new_y)
        distance_result.append([i,math.sqrt((i - new_x) * (i - new_x) + (basic_line[0] * i + basic_line[1] - new_y) * (basic_line[0] * i + basic_line[1] - new_y))])
        coor_result.append([new_x, new_y])

    return distance_result, coor_result
    

testimage = cv2.imread("testimage2.png", 1)
testimage = np.array(testimage)
print(testimage.shape[0])
# print(testimage[341 - 94 - 1][500])

length_y = testimage.shape[0]
# testimage
'''
test_slope = find_straightslope(261, length_y - 103, 364, length_y - 160)
dist_arr, coor_arr = find_distancefromboarderline(testimage, test_slope, 261, length_y - 103, 364)
'''
# testimage2
test_slope = find_straightslope(194, length_y - 157, 413, length_y - 131)
dist_arr, coor_arr = find_distancefromboarderline(testimage, test_slope, 194, length_y - 157, 413)
plt.scatter(list(zip(*dist_arr))[0], list(zip(*dist_arr))[1], 1)
plt.scatter(list(zip(*coor_arr))[0], list(zip(*coor_arr))[1])
plt.show()

# 곡률 찾는 함수, 정확도가 부정확한 것 같음
def find_curvature(coordinate_array):
    #x_t = np.gradient(list(zip(*coordinate_array))[0])
    #y_t = np.gradient(list(zip(*coordinate_array))[1])

    x_t = np.gradient(coordinate_array[:, 0])
    y_t = np.gradient(coordinate_array[:, 1])

    vel = np.array([ [x_t[i], y_t[i]] for i in range(x_t.size)])
    speed = np.sqrt(x_t * x_t + y_t * y_t)
    tangent = np.array([1/speed] * 2).transpose() * vel
    '''
    tangent_x = tangent[:, 0]
    tangent_y = tangent[:, 1]
    deriv_tangent_x = np.gradient(tangent_x)
    deriv_tangent_y = np.gradient(tangent_y)
    dT_dt = np.array([ [deriv_tangent_x[i], deriv_tangent_y[i]] for i in range(deriv_tangent_x.size)])
    length_dT_dt = np.sqrt(deriv_tangent_x * deriv_tangent_x + deriv_tangent_y * deriv_tangent_y)
    normal = np.array([1/length_dT_dt] * 2).transpose() * dT_dt
    '''

    ss_t = np.gradient(speed)
    xx_t = np.gradient(x_t)
    yy_t = np.gradient(y_t)

    curvature_val = np.abs(xx_t * y_t - x_t * yy_t) / (x_t * x_t + y_t * y_t)**1.5
    '''
    t_component = np.array([ss_t] * 2).transpose()
    n_component = np.array([curvature_val * speed * speed] * 2).transpose()
    acceleration = t_component * tangent + n_component * normal
    '''
    x_ayis = []
    for i in range(len(curvature_val)):
        x_ayis.append(i + 1)
    print(x_ayis)
    plt.scatter(x_ayis, curvature_val)
    plt.show()
    print(curvature_val)

coor_arr = np.array(coor_arr)
find_curvature(coor_arr)
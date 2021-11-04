def cameraSetting(request):
    # 각 조건을 만족하는지 검사하기 위함
    is_ankle_show = False
    is_ankle_mid = False
    is_shoulder_sideview = False

    left_ankle_x = request.data["keypoints"][15]["position"]["x"]
    left_ankle_y = request.data["keypoints"][15]["position"]["y"]

    ### 발목 보이는거를 위해
    below_ankle = 480 - left_ankle_y
    # print(f"발목 아래 공간:{below_ankle}")
    if below_ankle > 30:
        is_ankle_show = True
        print("발목이 보여요")
    else:
        is_ankle_show = False
        print("발목이 안 보여요!")

    ### 발목의 중앙 정렬을 위해 --> 정확도 향상을 하려면 left_ankle뿐만 아니라 right_ankle도 고려해야됨
    # print(f"발목 x좌표:{left_ankle_x}")
    if 250 < left_ankle_x < 390:
        is_ankle_mid = True
        print("중앙정렬 완료")
    else:
        is_ankle_mid = False
        print("발목이 중앙에 오도록 하세요!")

    left_shoulder_x = request.data["keypoints"][5]["position"]["x"]
    right_shoulder_x = request.data["keypoints"][6]["position"]["x"]
    mis_align = abs(left_shoulder_x - right_shoulder_x)

    ### 어깨의 측면view 정렬을 위해
    # print(mis_align)
    if mis_align < 20:
        is_shoulder_sideview = True
        print("측면으로 잘 섰습니다")
    else:
        is_shoulder_sideview = False
        print("몸을 틀어, 측면이 잘 보이도록 조정해주세요!")

    if is_ankle_show and is_ankle_mid == True:
        return True
    else:
        return False

import numpy as np
import math, cv2

test = cv2.imread("testimage_2.jpg", cv2.IMREAD_COLOR)
testarr = np.array(test)
#cv2.imshow("Hello",test)
print(testarr.shape)
print(testarr[0, 0])
print(testarr[279, 449])

divide_img = test[0:100,0:100]
cv2.imshow("Hello2", divide_img)
cv2.waitKey()
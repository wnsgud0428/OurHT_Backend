import base64
from django.db.models import base
import numpy, cv2
'''
testimage = cv2.imread("testimage.png", cv2.IMREAD_COLOR)
cv2.imshow("Hello", testimage)
cv2.waitKey()

imgarray = numpy.array(testimage)
print(imgarray.shape)
print(imgarray[170][255])


file = open("testimagearr.txt", "wb")
file.write(testimage)
file.close()
'''

f = cv2.imread("testimagege.jpg", 1)
f_encode = base64.b64encode(f)

f_decode = base64.b64decode(f_encode)
f_decode_arr = numpy.array(f_decode)
print(f_decode_arr)

'''
f_arr = numpy.frombuffer(base64.b64decode(f_encode), numpy.uint8)
cv2.imshow("test2", f_arr)
cv2.waitKey()
print("dd", f_arr)
'''
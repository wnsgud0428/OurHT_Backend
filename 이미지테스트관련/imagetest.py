import numpy, cv2

testimage = cv2.imread("testimage.png", cv2.IMREAD_COLOR)
cv2.imshow("Hello", testimage)
cv2.waitKey()

imgarray = numpy.array(testimage)
print(imgarray.shape)
print(imgarray[170][255])

'''
file = open("testimagearr.txt", "wb")
file.write(testimage)
file.close()
'''
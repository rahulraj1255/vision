from height import height
from resize import resize
import cv2
import numpy as np
import copy
import math
import sys
<<<<<<< HEAD
q=1
cv2.namedWindow('sdf')
for i in sys.argv:
	if q==1:
		q=0
		continue
	x = pupildetect(i)
	cv2.imshow('sdf',x)
	cv2.waitKey(3000)
cv2.destroyAllWindows()
=======


height('1.jpg',5)
>>>>>>> 3d7bec733d32263ded1fe80edcaf1b13fa0d3ef7

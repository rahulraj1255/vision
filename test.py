from b import pupildetect

import cv2
import numpy as np
import copy
import math
import sys
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

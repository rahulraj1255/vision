from outer import encContour
from matplotlib import pyplot as plt
import cv2
import numpy as np
import copy
import math
import sys
q=1
for i in sys.argv:
	if q==1:
		q=0
		continue
	x = cv2.imread(i)
	y=np.zeros(x.shape[0:2],dtype=np.uint8)
	ct=encContour(i)
	cv2.drawContours(y,[ct],0,(255),2)
	plt.imshow(y,'gray')
	plt.show()
	cv2.waitKey(3000)
cv2.destroyAllWindows()

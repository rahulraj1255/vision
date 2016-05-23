from b import pupildetect

import cv2
import numpy as np
import copy
import math
import sys

x = pupildetect('5.jpg')
cv2.imshow('final',x)
cv2.waitKey(0)
cv2.destroyAllWindows()

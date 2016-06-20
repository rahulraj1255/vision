import cv2
import numpy as np
from man_hands import cor_hands
from outer import encContour
img=cor_hands('scaled_mfrontf.jpg', 'mside.jpg','ar1.jpg', 'mside.jpg')
cv2.imwrite('TEST_new.jpg',img)

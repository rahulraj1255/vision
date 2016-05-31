from outer import encContour
from matplotlib import pyplot as plt
import cv2
import numpy as np
import copy
import math
import sys
from plot3d import plot3dHuman
from ret2Val import ret2Val
k=ret2Val('girl_front.jpg')
plot3dHuman('girl_front.jpg','girl_side.jpg',k)

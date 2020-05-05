import numpy as np
from skimage.io import imsave, imread
from skimage import img_as_float
import sys
sys.path.append('..')
from imresize import *

gtname='butterfly.png'
img_uint8 = imread(gtname)
new_img_uint8 = imresize(img_uint8, scalar_scale=0.5)
new_img_uint8 = imresize(new_img_uint8, scalar_scale=2)
imsave('mat_bic_uint8_'+gtname, new_img_uint8)
img_double = img_as_float(img_uint8)
new_img_double = imresize(img_double, scalar_scale=0.5)
new_img_double = imresize(new_img_double, scalar_scale=2)
imsave('mat_bic_double_'+gtname, convertDouble2Byte(new_img_double))
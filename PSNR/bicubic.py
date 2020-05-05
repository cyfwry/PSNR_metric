import cv2
import numpy as np
import glob
from PIL import Image

def matlab_YCrCb(img):
    '''
    input:
    img:float64,0~255,H*W*C,BGR
    '''
    #The reproduction about rgb2ycbcr in matlab
    result=np.zeros(img.shape)
    result[:,:,0] = (65.481*img[:,:,2] + 128.553*img[:,:,1] + 24.966*img[:,:,0])/255. + 16.
    result[:,:,1] = (-37.797*img[:,:,2] -74.203*img[:,:,1] + 112*img[:,:,0])/255. + 128.
    result[:,:,2] = (112*img[:,:,2] -93.786*img[:,:,1] -18.214*img[:,:,0])/255. + 128.
    result=np.round(result)
    result=result.astype(np.uint8)

    return result

scale=2
gt_path='gt'
gt_list=glob.glob(gt_path+'/*.*')
gt_list=np.asarray(gt_list)

PSNR=0
for gtname in gt_list:
    gt=cv2.imread(gtname)
    gt=gt[:gt.shape[0]//scale*scale,:gt.shape[1]//scale*scale,:]
    
    # python-opencv YCrCb
    # img=cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
    # gt=cv2.cvtColor(gt,cv2.COLOR_BGR2YCrCb)
    # gt=gt.astype(np.float64)
    # img=cv2.resize(gt,(gt.shape[1]//scale,gt.shape[0]//scale),cv2.INTER_CUBIC)
    # img=cv2.resize(img,(gt.shape[1],gt.shape[0]),cv2.INTER_CUBIC)
    
    # Image resize+Matlab YCrCb
    gt=gt.astype(np.float64)
    gt=matlab_YCrCb(gt)
    gt=gt[:,:,0]
    gt=gt.astype(np.float64)
    img=(Image.fromarray(gt)).resize((gt.shape[1]//scale,gt.shape[0]//scale),Image.BICUBIC)
    img=np.asarray(img.resize((gt.shape[1],gt.shape[0]),Image.BICUBIC))

    # uint8
    img=img.astype(np.uint8)
    gt=gt.astype(np.uint8)    
    
    # shave border
    img=img[scale:-scale,scale:-scale]
    gt=gt[scale:-scale,scale:-scale]
    
    img=img.astype(np.float64)
    gt=gt.astype(np.float64)
    img_PSNR=10*np.log10((255**2)/np.mean((gt-img)**2))
    print(img_PSNR)
    PSNR+=img_PSNR

print(PSNR/len(gt_list))
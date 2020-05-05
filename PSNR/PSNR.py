import cv2
import numpy as np
import glob

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
img_path='img'
img_list=glob.glob(img_path+'/*.*')
img_list=np.asarray(img_list)

PSNR=0
for gtname in gt_list:
    gt=cv2.imread(gtname)
    # name match
    imgname=img_list[[gtname[3:-4] in x for x in img_list]][0]
    img=cv2.imread(imgname)
    gt=gt.astype(np.float64)
    img=img.astype(np.float64)
    
    # python-opencv YCrCb
    # img=cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
    # gt=cv2.cvtColor(gt,cv2.COLOR_BGR2YCrCb)
    # Matlab YCrCb
    img=matlab_YCrCb(img)
    gt=matlab_YCrCb(gt)
    
    gt=gt[:img.shape[0],:img.shape[1],:]
    # shave border
    gt=gt[scale:-scale,scale:-scale,:]
    img=img[scale:-scale,scale:-scale,:]
    
    img=img[:,:,0]
    gt=gt[:,:,0]
    
    gt=gt.astype(np.float64)
    img=img.astype(np.float64)

    # print((gt-img).max())
    # print((gt-img).min())
    
    img_PSNR=10*np.log10((255**2)/np.mean((gt-img)**2))
    PSNR+=img_PSNR
    print(img_PSNR)

print(PSNR/len(gt_list))
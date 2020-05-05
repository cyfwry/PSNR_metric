% path of test image,generate in img_test_and_save.m
path='.';
% scale factor
scale=2;
fileFolder=fullfile(path);
dirOutput=dir(fullfile(fileFolder,'*.bmp'));
fileNames={dirOutput.name};
len=size(fileNames);
len=len(2);
sum=0;
for i=1:len
	% read image, transform to YCrCb, calculate PSNR
	% path of gt image,you may need to change the content in '/Set5/'
    gt_path=strcat(path,'/Set5/',fileNames(:,i));
    gt=imread(gt_path{1});
    img_path=fileNames(:,i);
    img=imread(img_path{1});
    
    gt=gt(1+scale:end-scale,1+scale:end-scale,:);
    img=img(1+scale:end-scale,1+scale:end-scale,:);

    if size(gt,3)==3
        gt=rgb2ycbcr(gt);
        gt=gt(:,:,1);
        img=rgb2ycbcr(img);
        img=img(:,:,1);
    end

    imgdiff=double(gt)-double(img);
    mse=mean(mean(imgdiff.^2));
    y=10*log10(255*255/mse);
    sum=sum+y;
    
end
% PSNR,should be 33.6529 when test Set5
sum/len
% path of image
path='./Set5';
% scale factor
scale=2;
fileFolder=fullfile(path);
dirOutput=dir(fullfile(fileFolder,'*.bmp'));
fileNames={dirOutput.name};
len=size(fileNames);
len=len(2);
sum=0;
for i=1:len
	% read image and test
    img_path=strcat(path,'/',fileNames(:,i));
    img_psnr=PSNR(img_path{1},scale)
    sum=sum+img_psnr;
    % read image, bicubic downsample and upsample, save image
	% you can annotate it if you do not need this
    img=imread(img_path{1});
    crop_size=size(img);
    crop_size=crop_size-mod(crop_size,scale);
    img=img(1:crop_size(1),1:crop_size(2),:);
	% if you want generate double bicubic image, you need to unannotate it
	% img=double(img)
    img=imresize(img,1/scale,'bicubic');
    img=imresize(img,scale,'bicubic');
    save_name=fileNames(:,i);
    imwrite(img,save_name{1});  
end
% PSNR,should be 33.6614 when test Set5
sum/len
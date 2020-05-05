function y=PSNR(img_path,scale)
img=imread(img_path);

img_y=img;

% this code is a reproduction of the function rgb2ycbcr
% origT = [65.481 128.553 24.966;...
%     -37.797 -74.203 112; ...
%     112 -93.786 -18.214];
% origOffset = [16;128;128];
% img_test_y=zeros(size(img));
% for i = 1:size(img,1)
%     for j =1:size(img,2)
%         point=double(img(i,j,:))/255.;
%         point=reshape(point,1,3);
%         img_test_y(i,j,:)=origT*point'+origOffset;
%     end
% end
% img_test_y=img_test_y(:,:,1);
% img_test_y=round(img_test_y);
% result=mean(mean(abs(double(img_y)-img_test_y)));

%crop picture
crop_size=size(img_y);
crop_size=crop_size-mod(crop_size,scale);
img_y=img_y(1:crop_size(1),1:crop_size(2),:);

%double
img_y=double(img_y);

%bicubic imresize
img_l=imresize(img_y,1/scale,'bicubic');
img_b=imresize(img_l,scale,'bicubic');

%uint8
img_b=uint8(img_b);
img_y=uint8(img_y);

%shave border
img_b=img_b(1+scale:end-scale,1+scale:end-scale,:);
img_y=img_y(1+scale:end-scale,1+scale:end-scale,:);

%transform to YCbCr
if size(img_y,3)==3
    img_b=rgb2ycbcr(img_b);
    img_b=img_b(:,:,1);
    img_y=rgb2ycbcr(img_y);
    img_y=img_y(:,:,1);
end

%calculater PSNR
imgdiff=double(img_y)-double(img_b);
mse=mean(mean(imgdiff.^2));

y=10*log10(255*255/mse);
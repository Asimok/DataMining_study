import cv2

# 需要裁剪的图片路径
infile = '/home/asimov/PycharmProjects/DataMining/深度学习/RNN/testimages/31.jpg'
# 裁剪后图片的保存路径
outfile = '/home/asimov/PycharmProjects/DataMining/深度学习/RNN/cut_imgs/31.jpg'

# 目标裁剪图片的宽和高
weight = 28
hight = 28
crop_size = (weight, hight)
img = cv2.imread(infile)
img_new = cv2.resize(img, crop_size, interpolation=cv2.INTER_AREA)
cv2.imwrite(outfile, img_new)

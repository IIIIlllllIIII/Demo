from PIL import Image, ImageFilter
import os
# 打开指定路径下的图片文件
im_1 = Image.open(r'C:\Users\rog\Desktop\Demo\test.jpg')
# 获取原图片的宽度和高度
w, h = im_1.size
# 输出原图片尺寸信息
print('Original image size: %sx%s' %(w, h))

im_1.thumbnail((w//2, h//2))    # 将原图片按比例缩小到一半，生成缩略图
# 输出缩略图尺寸信息
print('Resize image to: %sx%s' % (w//2, h//2))

im_1.save('thumbnail.jpg','jpeg')   # 保存缩略图至当前工作目录，并以JPEG格式存储
print(os.getcwd())  # 输出当前工作目录路径
im_2 = im_1.filter(ImageFilter.BLUR)    # 应用模糊滤镜对原图片进行处理
im_2.save('blur.jpg', 'jpeg')   # 保存模糊处理后的图片至当前工作目录，并以JPEG格式存储


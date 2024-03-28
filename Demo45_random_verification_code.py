#生成一个带有随机字母和颜色的验证码图片，并对其进行了模糊处理，最后保存为 code.jpg 文件。
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random

def rdmchar():  #随机生成一个大写字母
    return chr(random.randint(65,90))
def rdmcolor1(): #随机生成一个深色
    return (random.randint(64,255), random.randint(64,255), random.randint(64,255))
def rdmcolor2(): #随机生成另一个浅色
    return (random.randint(32,127), random.randint(32,127), random.randint(32,127))

#定义长宽
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))  #创建一个背景白色的图片对象，色彩空间为RGB
font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 36)  #创建并设置字体(Font)
draw = ImageDraw.Draw(image)    #创建Draw对象（这里通过对象方法操作Image）
for x in range(width):  #循环绘制每一个像素点
    for y in range(height):
        draw.point((x, y), fill= rdmcolor1())
for n in range(4):  #循环绘制4个字符
    draw.text((60*n + 10, 10), rdmchar(), font=font, fill= rdmcolor2())
image = image.filter(ImageFilter.BLUR)  #进行模糊处理
image.save('code.jpg', 'jpeg')
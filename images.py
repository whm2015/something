# -*- coding: utf-8 -*-


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
img=Image.open(r'D:\毕设\图\p.png').convert('RGBA') #打开图像并转化为数字矩阵

print(img.getpixel((2,58)))

rows, cols = img.size
for i in range(rows):
    for j in range(cols):
        if img.getpixel((i, j))[2] < 200:
            # set color black
            pass
            img.putpixel((i, j), (10, 10, 10, 255))
        if img.getpixel((i, j))[0] >= 100:
            # set 透明
            pass
            img.putpixel((i, j), (0, 0, 0, 0))

img.save('test.png')

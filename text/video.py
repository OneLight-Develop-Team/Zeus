import os
import cv2
import numpy as np

path = r'C:\Users\huangPeiXin\Desktop\img3/'
filelist = os.listdir(path)

fps = 24 #视频每秒24帧
size = (500,500)
#可以使用cv2.resize()进行修改

# video = cv2.VideoWriter( r'C:\Users\huangPeiXin\Desktop\img3\VideoTest1.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
#视频保存在当前目录下

# video = cv2.VideoWriter("test.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, size)

# video = cv2.VideoWriter("test.mp4", 0x00000021, fps, size)



for item in filelist:
    if item.endswith('.jpg'):
        
        item = path + item
        img = cv2.imread(item)
        for i in range(24):
            video.write(img)
                    

video.release()
cv2.destroyAllWindows()
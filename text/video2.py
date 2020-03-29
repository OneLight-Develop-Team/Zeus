# coding=utf-8
import os
import cv2
from PIL import Image
 
def makevideo(path, fps):
    """ 将图片合成视频. path: 视频路径，fps: 帧率 """
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    path1 = 'C:/Users/huangPeiXin/Desktop/img3'
    im = Image.open('C:/Users/huangPeiXin/Desktop/img3/0000000.jpg')
    vw = cv2.VideoWriter(path, fourcc, fps, im.size)
    for i in os.listdir(path1):
        frame = cv2.imread(path1 +'/'+ i)
        vw.write(frame)
 
if __name__ == '__main__':
    video_path = 'C:/Users/huangPeiXin/Desktop/546.mp4'
    makevideo(video_path, 10)  # 图片转视频


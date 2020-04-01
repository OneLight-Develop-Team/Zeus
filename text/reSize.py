#coding=utf-8


from PIL import Image 

import os

current_path = os.path.dirname(os.path.abspath(__file__))
file_path =  os.path.dirname(current_path)

def make_thumb(path, size = 500):
    """
    缩略图生成程序
    size 参数传递要生成的尺寸
    返回缩略图地址
    """    
    # base, ext = os.path.splitext(path) # 获取文件路径与文件名
    
    try: # 尝试打开文件
        im = Image.open(path)
    except IOError:
        return
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
           
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')
            
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)            
        region = im.crop(box)





    filename = (path.split("/"))[-1]

    savePath = "C:\\Users\\huangPeiXin\\Desktop\\img3\\" + os.path.splitext(filename)[0] + ".jpg"
    # savePath = file_path + r"\res\images\thumbnail"  + "_" + "%sx%s" % (str(size), str(size)) + ".jpg"
    thumb = region.resize((size,size), Image.ANTIALIAS)
    thumb.save(savePath, quality=75)  # 默认 JPEG 保存质量是 75, 可选值(0~100)
    
    
    return savePath

if __name__ == "__main__":
    filelist = os.listdir(r"C:\Users\huangPeiXin\Desktop\img")
    for item in filelist:
        make_thumb(r"C:\Users\huangPeiXin\Desktop\img/" + item)
        
# <-- coding utf-8 -->

from Qt.QtWidgets import QApplication
import json,os

current_path = os.path.dirname(os.path.abspath(__file__))
file_path =  os.path.dirname(current_path)

class Data():
    """储存数据设置类"""
        
    #屏幕大小
    @classmethod
    def getWindowWidth(cls):
        return QApplication.desktop().width()
    @classmethod
    def getWindowHeight(cls):
        return QApplication.desktop().height()

    
    # #获取打开时的文件路径
    # @classmethod
    # def getOpenPath(cls):
    #     with open(file_path + r"\res\temp\setting.json") as js:
    #         setting_dir = json.load(js)

    #     if "filePath" in setting_dir.keys():
    #         return setting_dir["filePath"]
    #     else:
    #         return "C"
    
    # #设置打开时的文件路径
    # @classmethod
    # def setOpenPath(cls,path):
    #     with open(file_path + r"\res\temp\setting.json") as js:
    #         setting_dir = json.load(js)

    #     setting_dir["filePath"] = path

    #     #写入数据到json文件中
    #     with open(file_path + r"\res\temp\setting.json", 'w') as json_file:
    #         json.dump(setting_dir,json_file,indent=4)
    
    
    # #获取所有标签
    # @classmethod
    # def getTag(cls):
    #     with open(file_path + r"\res\temp\setting.json") as js:
    #         setting_dir = json.load(js)


    #     return setting_dir["default_tag"] + setting_dir["custom_tag"]

    # #添加标签
    # @classmethod
    # def addTag(cls,tag):
    #     with open(file_path + r"\res\temp\setting.json") as js:
    #         setting_dir = json.load(js)
            
    #     setting_dir["custom_tag"].append("tag")

    #     #写入数据到json文件中
    #     with open(file_path + r"\res\temp\setting.json", 'w') as json_file:
    #         json.dump(setting_dir, json_file, indent=4)

    # # 获取自定义的标签
    # @classmethod
    # def getCustomTag(cls):
    #     with open(file_path + r"\res\temp\setting.json") as js:
    #         setting_dir = json.load(js)


    #     return setting_dir["custom_tag"]

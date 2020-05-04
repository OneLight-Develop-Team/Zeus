#coding=utf-8

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import os

def sendEmail(name, paths):
    
    # print(name,paths,)
    path = ""
    for p in paths:
        filepath = os.path.dirname(p)
        filename = filepath.split("/")[-1]
        path += filename
        path += " "

    #todo:根据用户名获取收件人邮箱
    #收件人邮箱
    receiver = '2420763705@qq.com'  #需要替换
    
    #qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    #sender_qq为发件人的qq号码
    sender_qq = '1716973911'
    #pwd为qq邮箱的授权码
    pwd = 'drgmjaskqnqfbaea' 
    #发件人的邮箱
    sender_qq_mail = '1716973911@qq.com'
  

    #邮件的正文内容
    mail_content = '你好,' + name + ',' + '你已成功将资源文件 ' + path + '导入到资源浏览器中'
    #邮件标题
    mail_title = 'Zeus的邮件'




    try:

        #ssl登录
        smtp = SMTP_SSL(host_server)
        #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(0)
        smtp.ehlo(host_server)
        smtp.login(sender_qq, pwd)

        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        msg["To"] = receiver
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()
    except:
        print ("邮件发送失败")
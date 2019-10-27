from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
'''
TODO:
ok    发邮件给我自己 通知
ok 打包成.exe 然后每天自动化运行
1. 对讲座时间与now进行对比，推送还没进行的讲座
'''
def get_PO_teacher():
    with open('teacher_name.txt',encoding = 'utf-8') as f:
        PO_teacher = f.read().split(',')
    return PO_teacher

def get_new_lecture_info(lecture_url,kv):
    r_of_latest_lecture = requests.get(lecture_url,headers=kv)
    r_of_latest_lecture.encoding = r_of_latest_lecture.apparent_encoding
    ## soup for find all lecture
    soup_lecture = BeautifulSoup(r_of_latest_lecture.text,'html.parser')

    events = soup_lecture.find_all('tr',{'valign':'middle'})
    lecture_url_root = 'https://mel.xmu.edu.cn/'


    for index in range(0,len(events)-4,2):
        #print(index)
        name = str(events[index])[201:211].strip(' ')
        if name in PO_teacher:
            news = name+ '老师邀请专家开讲座啦'

            break
        else:
            name_list = name.split('、')
    #        host_people = host_people + name_list
            for name in name_list:
                if name in PO_teacher:
                    news = name+ '老师邀请专家开讲座啦'

                    break # brask at first event 

    ## soup to find time, url, etc
    time = soup_lecture.find_all('td', {'width':'768'})
    url_lecture = soup_lecture.find_all('td', {'height':'30'})

    time_index = int(index/2)
    time_for_lecture = '时间：' + time[time_index].string.strip(' ') 
    #print(time_for_lecture)
        #因为多了没啥用
    url_index = time_index + 1
    title_lecture = '标题：' + url_lecture[url_index].a.string.strip(' ')
    #print(title_lecture)
    url_of_lecture = '链接：'+lecture_url_root+url_lecture[url_index].a.attrs['href']
    #print(url_of_lecture)
    return [news, time_for_lecture,title_lecture,url_of_lecture]

def print_info(new_lecture_info):
    #print(new_lecture_info)
    lecture_info = '\n'.join(new_lecture_info)
    print(lecture_info)
def save_lec_info(new_lecture_info):
    lecture_info = '\n'.join(new_lecture_info)
    with open('lecture_info.txt','w',encoding='utf-8') as f:
        f.write(lecture_info)

def send_email(new_lecture_info):
    mail_host = 'smtp.qq.com'
    mail_user = '1093656867@qq.com'
    mail_pass = 'your own pass code'
    sender = '1093656867@qq.com'
    receivers  = ['1093656867@qq.com']
    message = MIMEText('\n'.join(new_lecture_info), 'plain', 'utf-8')
    message['From'] = Header("Jeff 的自动程序", 'utf-8')
    message['To'] =  Header("我自己", 'utf-8')
    subject = 'NEW MEL Lecture infomation~~' + new_lecture_info[0]
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        return "邮件发送成功"
    except smtplib.SMTPException:
        return "Error: 无法发送邮件"


if __name__ == "__main__":
    kv = {'user-agent':'Mozilla/5.0'}
    lecture_url = 'https://mel.xmu.edu.cn/lecture.asp?id=1'

    PO_teacher = get_PO_teacher()
    new_lecture_info = get_new_lecture_info(lecture_url,kv)

    print_info(new_lecture_info)
    with open('lecture_info.txt','r',encoding='utf-8') as f:
        already_lec_info = f.read()

    if '\n'.join(new_lecture_info) == already_lec_info:
        print('无新讲座')
        send_email_flag = 0
    else:
        print('发现新讲座，准备发送邮件通知')
        save_lec_info(new_lecture_info)
        send_email_flag = 1

    if send_email_flag:
        print(send_email(new_lecture_info))
    while 1:
        pass # to hold on the cmd

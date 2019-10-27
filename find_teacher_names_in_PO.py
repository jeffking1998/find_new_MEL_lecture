from bs4 import BeautifulSoup
import requests


kv = {'user-agent':'Mozilla/5.0'}
contens = []
for i in range(1,4):
    #        root_url                                       index 从教授-助理教授      物海url
    pages = 'http://coe.xmu.edu.cn/TeacherList.aspx?Id=T' + str(i)                + '&deptid=P24'
    r = requests.get(pages,headers=kv)
    #soup=BeautifulSoup((html_doc.replace('<br>','')).replace('<br/>',''),'lxml')

    soup = BeautifulSoup(r.text.replace('<br />',''),'html.parser')
    names = soup.find_all('a',{'style':'color: blue'})## 用'a'就 够用了
    
    for name in names:
        #print(name.string.strip(' ').strip('\n'))
        contens.append(name.string.strip('\r').strip('\n').strip(' ')[0:3].strip('\r'))

    #print(names,'*************\n*************')
#    contens.append(names.a.string)


with open('teancher_name.txt','w',encoding='utf-8') as f:
    f.write(','.join(contens))

import requests
import json
from bs4 import BeautifulSoup

s = requests.Session()

myid = '16050506126'
mypwd = '16050506126'

def login(id, pwd):
    url = 'http://10.0.10.57/servlet/adminservlet'
    data = {
        'operType': 911,
        'loginflag': 0,
        'loginType': 0,
        'userName': id,
        'passwd': pwd
    }
    r = s.post(url, data=data)

def getMessage(id):
    message = []
    url = '%s%s%s' % ('http://10.0.10.57/SportWeb/health_info/listdetalhistroyScore.jsp?studentNo=', id, '&gradeNo=1')

    try:
        r = s.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        content = r.text
        soup = BeautifulSoup(content, "html.parser")
        uname = soup.find_all('b')
        uname = uname[1].string
        uname = uname.replace('\u3000', '')

        message.append({
            '信息': uname
            })
        
        for form in (soup.find_all('form')):
            tds = form.find_all('td')
            message.append({
                '序号': tds[0].string,
                '项目名称': tds[1].string,
                '测试成绩': tds[2].string,
                '分数': tds[3].string,
                '结论': tds[4].string
                })

        return message
    except:
        return "ERROR"
    
def run():
    message = []
    login(myid, mypwd)
 
    for num in range(17050506101, 17050506150):
        message = getMessage(num)
        if (message == "ERROR"):
            continue
        path = 'E:/spider/%s.txt' %(num)
        d = json.dumps(message, ensure_ascii=False)
        print(d)
        f = open(path, 'w')
        
        f.write(d)
        f.close()

        
if __name__ == '__main__':
    run()

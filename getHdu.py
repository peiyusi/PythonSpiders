#!usr/bin/python3
import requests
from bs4 import BeautifulSoup
import bs4
import re 

s = requests.Session()

vis = {}
myid = 'Lakersfan42'
mypwd = 'pys1999'

def login(id, password):
    url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
    data = {
        'username': id,
        'userpass': password, 
        'login': 'Sign in'
    }

    r = s.post(url, data=data)


def getCode(rid):
    url = "http://acm.hdu.edu.cn/viewcode.php?rid=" + rid
    r = s.get(url)
    txt = r.text
    pattern = re.compile('<textarea id=usercode style="display:none;text-align:left;">(.+?)</textarea>',re.S)
    ans = pattern.findall(txt)[0]
    return ans



def run(id):
    url = 'http://acm.hdu.edu.cn/status.php?user='+id+'&status=5'
    flag = True
    while flag:
        try:
            r = s.get(url)
        except Exception:
            continue
        txt = r.text
        pattern = re.compile('/showproblem.php\\?pid=(.+?)">(.+?)</a></td><td>(.+?)</td><td>(.+?)</td><td><a href="/viewcode.php\\?rid=(.+?)"',re.S)
        ans = pattern.findall(txt)
        for line in ans:
            tihao = line[0]
            if tihao in vis:
                continue
            else:
                path = '/var/hdu/%s.cpp' %(tihao)
                vis[tihao] = True
                rid = line[-1]
                code = getCode(rid)
#                code = code.replace('\r\n', '\n')             
                #code = code.replace('&gt:', '>')
                #code = code.replace('&lt:', '<')
                #code = code.replace('&amp;', '&')
                f = open(path, 'w')
                f.write(code)
        pattern = re.compile('Prev Page</a><a style="margin-right:20px" href="(.+?)">Next Page',re.S)
        ans = pattern.findall(txt)
        if ans == []:
            print("test")
            flag = False;
        else:
            url = 'http://acm.hdu.edu.cn' + ans[0]



    




if   __name__ == '__main__':
    login(myid, mypwd)
    run(myid)

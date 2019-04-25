# -*- coding:utf-8 -*- 
import requests
import json
import re
from bs4 import BeautifulSoup
import xlwings as xw
import mysql.connector

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
wb = xw.Book('16级新生名单.xls')
sht = wb.sheets['名单']
s = requests.Session()
mydb = mysql.connector.connect(
  host="120.79.227.59",
  port="3306",
  user="root",
  passwd="abc",
  database="grade"
)
mycursor = mydb.cursor()
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
    r = s.post(url, data=data, headers=headers)
    
def getMessage(id):
    message = []
    url = '%s%s%s' % ('http://10.0.10.57/SportWeb/health_info/listdetalhistroyScore.jsp?studentNo=', id, '&gradeNo=3')

    try:
        r = s.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        content = r.text
        soup = BeautifulSoup(content, "html.parser")
        i = 0
        th = soup.find("th", text="总计")
        totalScore = ""
        evaluation = ""
        for sibling in th.next_siblings:
          if (i == 5):
              totalScore = sibling.string
          if (i == 7):
              evaluation = sibling.string
              break
          i = i + 1

        message.append({
            '总分': totalScore,
            '结论': evaluation
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

def insertTotalGrade(stuNo, totalGradeDict):
    grade = ""
    result = ""
    for key in totalGradeDict:
        if (key == "总分"):
            grade = totalGradeDict[key]
        if (key == "结论"):
            result = totalGradeDict[key]
    
    sql = "INSERT INTO grade(type, stuno, grade, result, semester) VALUES ('总分', '%s', '%s', '%s', 2)" % (stuNo, grade, result)
    try:
        mycursor.execute(sql)
        mydb.commit()    
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    

def insertGrade(stuNo, gradeDict):
    sqlhead = "INSERT INTO grade(type, stuno, grade, score, result, semester) "
    sqlmid = "VALUES('%s', " 
    sqltail = "'%s', '%s', '%s', '%s', 2)"
    
    for key in gradeDict:
        if (key == "总分"):
            insertTotalGrade(stuNo, gradeDict)
            return
        elif (gradeDict[key] == "身高(cm)"):
            sqlmid = sqlmid % ("height")
        elif (gradeDict[key] == "体重(kg)"):
            sqlmid = sqlmid % ("weight")
        elif (gradeDict[key] == "肺活量"):
            sqlmid = sqlmid % ("vitalcapacity")
        elif (gradeDict[key] == "50米跑(秒)"):
            sqlmid = sqlmid % ("shortrun")
        elif (gradeDict[key] == "立定跳远(cm)"):
            sqlmid = sqlmid % ("jump")
        elif (gradeDict[key] == "千米跑(分)"):
            sqlmid = sqlmid % ("longrun")
        elif (gradeDict[key] == "坐体前屈(cm)"):
            sqlmid = sqlmid % ("stand")
        elif (gradeDict[key] == "引体向上/仰卧起坐"):
            sqlmid = sqlmid % ("pull")
        elif (gradeDict[key] == "耐力加分"):
            sqlmid = sqlmid % ("endurance")     
        elif (key== "测试成绩"):
            grade = gradeDict[key]
        elif (key== "分数"):
            score = gradeDict[key]
        elif (key== "结论"):
            result = gradeDict[key]

    sqltail = sqltail % (stuNo, grade, score, result)
    sql = sqlhead + sqlmid + sqltail
    
    try:
        mycursor.execute(sql)
        mydb.commit()    
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

def run():
    message = []
    login(myid, mypwd)
    count = 2
    stuDepartment = ""
    stuClass = ""
    stuNum = ""
    stuName = ""
    stuGender = ""
    while (count != 4620):
##       stuDepartment = sht.range('A'+str(count)).value
##       stuClass = sht.range('B'+str(count)).value
       stuNum = sht.range('C'+str(count)).value
##       stuName = sht.range('D'+str(count)).value
##       stuGender = sht.range('E'+str(count)).value
##       Studentsql = "INSERT INTO student(department, class, stuno, name, gender) VALUES ('%s', '%s', '%s', '%s', '%s')" % (stuDepartment, stuClass, stuNum, stuName, stuGender)
##       try:
##         mycursor.execute(Studentsql)
##         mydb.commit()
##       except mysql.connector.Error as e:
##         print('connect fails!{}'.format(e)) 
       count += 1
       print(stuNum)
       message = getMessage(stuNum)
       if (message == "ERROR"):
         continue
       print(message)
##       for item in message:
##         insertGrade(stuNum, item)   
                
if __name__ == '__main__':
    run()

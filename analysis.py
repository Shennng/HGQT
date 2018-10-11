import re
from operator import itemgetter
#from bs4 import BeautifulSoup

from orignal_data import main

def parser_data(verifycode_, cookies_, usr ,pwd, kksj):
    '分析数据'
    text = main(verifycode_, cookies_, usr, pwd, kksj)
    regex = re.compile(r'title="null" >(.*?)</td>')
    orignal_data = regex.findall(text)
    
    data = []
    if orignal_data:
        for i in range(0,len(orignal_data)):
            if orignal_data[i] == usr:
                data.append(orignal_data[i:(i+10)])
        n = 0
        while True:
            try:
                if data[n][-1] != '正常':
                    data[n].insert(6, '--')
                else:
                    data[n].append(' ')
                n += 1
            except:
                break
        data = sorted(data, key=itemgetter(2, 3), reverse=True)
    #standard = '{0:^5}\t{1:^5}\t{2:^20}{3:^5}\t{4:^5}\t{5:^5}\t{6:^5}\t{7:^5}\t{8:^5}\t{9:^5}\t{10:^5}'
    #columns = ['学号', '姓名', '开课学期', '课程名称', '总成绩', '课程性质', '课程类别', '学时', '学分', '考试性质', '补重学期']
    #print(standard.format(columns[0], columns[1], columns[2], columns[3], columns[4], columns[5], columns[6], columns[7], columns[8], columns[9], columns[10]))
    #for each in data:
    #    print(standard.format(each[0], each[1], each[2], each[3], each[4], each[5], each[6], each[7], each[8], each[9], each[10]))
    return data

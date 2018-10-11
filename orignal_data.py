#import sys
#import io
import re
import requests
#from PIL import Image

#改变标准输出的默认编码
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

def get_cookies():
    '从kdjw/的Set-Cookie获取整个会话的cookies'
    
    kdjw_hed = {'Host': 'kdjw.hnust.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    r = s.get(r'http://kdjw.hnust.cn/kdjw/',headers=kdjw_hed, timeout=3)
    #print(r.headers)
    #获取到cookies
    cookies = r.headers['Set-Cookie'][0:-12]
    return cookies

def get_verifycode(cookies):
    '根据所得cookies获取验证码'
    
    verifycode_hed = {'Cookie': cookies,
        'Host': 'kdjw.hnust.cn',
        'Referer': 'http://kdjw.hnust.cn/kdjw/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    #验证码获取
    r_verifycode = s.get(r'http://kdjw.hnust.cn/kdjw/verifycode.servlet', headers=verifycode_hed, timeout=3)
    
    with open('code.jpg','wb') as f:
        f.write(r_verifycode.content)
    return True

#def show_verifycode():
#    '通过Image模块展示验证码图片，并提示用户输入验证码'
#    
#    im = Image.open('code.jpg')
#    im.show()
#    verifycode = input('请输入验证码: ')
#    return verifycode
    
def virtual_login(verifycode, cookies, usr, pwd):
    '虚拟登陆教务网'
    #模拟登陆
    login_data = {'useDogCode': '',
        'USERNAME': usr,
        'PASSWORD': pwd,
        'RANDOMCODE': verifycode}
    post_hed = {'Cookie': cookies,
        'Host': 'kdjw.hnust.cn',
        'Origin': 'http://kdjw.hnust.cn',
        'Referer': 'http://kdjw.hnust.cn/kdjw/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    r_login = s.post(r'http://kdjw.hnust.cn/kdjw/Logon.do?method=logon', headers=post_hed, data=login_data, timeout=3)
    #验证登陆
    r_verifylogin = s.get(r'http://kdjw.hnust.cn/kdjw/framework/main.jsp', headers=post_hed)
    regex = re.compile(r'<title>湖南科技大学数字化校园平台-强智科技</title>')
    verifylogin = regex.search(r_verifylogin.text)
    if verifylogin:
        return False
    else:
        return True
    
def search_and_get_grades_html(cookies, kksj):
    '模拟登陆之后，打开成绩查询页面获取成绩数据'
    #成绩查询
    #针对不止一页成绩数据的情况进行优化
    form_data = {'kksj': kksj, 'kcxz': '', 'kcmc': '', 'xsfs': 'qbcj', 'ok':'', }
    query_hed = {'Cookie': cookies,
        'Host': 'kdjw.hnust.cn',
        'Origin': 'http://kdjw.hnust.cn',
        'Referer': 'http://kdjw.hnust.cn/kdjw/jiaowu/cjgl/xszq/query_xscj.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
    r_grade = s.post('http://kdjw.hnust.cn/kdjw/xszqcjglAction.do?method=queryxscj', headers=query_hed, data=form_data, timeout=3)
    #获取总页数
    regex = re.compile(r'name = "totalPages" value="(.*?)"')
    totalpages = int(regex.findall(r_grade.text)[-1])
    #按页数获取成绩数据
    if totalpages == 1:
        print('成功获取第1页成绩数据！！！ 共1页.',cookies)
        return r_grade.text
    else:
        html_texts = r_grade.text
        print('成功获取第1页成绩数据！！！ 共%d页.' % totalpages, cookies)
        query_hed.update({'Referer': 'http://kdjw.hnust.cn/kdjw/xszqcjglAction.do?method=queryxscj'})
        #print(query_hed)
        for pagenum in range(2,totalpages+1):
            page_param = {'PageNum':pagenum, 'kksj':kksj}
            r_page = s.get(r'http://kdjw.hnust.cn/kdjw/xszqcjglAction.do?method=queryxscj', headers=query_hed, params=page_param, timeout=3)
            html_texts += r_page.text
            print('成功获取第%d页成绩数据！！！ 共%d页.' % (pagenum, totalpages), kksj, cookies)
        return html_texts
        
def get_code_in_file():
    global s, cookies_
    s = requests.Session()
    #cookies
    cookies_ = get_cookies()
    #更新验证码code.jpg
    get_verifycode(cookies_)
    return cookies_

def main(verifycode_, cookies_, usr_, pwd_, kksj_):
    #登陆获取数据
    orignal_html = ''
    login = virtual_login(verifycode_, cookies_, usr_, pwd_)
    if login:
        orignal_html = search_and_get_grades_html(cookies_, kksj_)
    #print(orignal_html)
    return orignal_html

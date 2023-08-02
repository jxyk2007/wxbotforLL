import requests
import datetime
import calendar
#from datetime import datetime
import json
def sendWx(RevenueInformation):
##微信bot 发送信息函数
    url = "http://127.0.0.1:5555/api/sendATMsg"

    payload = json.dumps({
      "para": {
        "id": "{{date_time}}",
        "roomid": "null",
        "wxid": "123456@chatroom",  ##wx群id
        "content": RevenueInformation,
        "type": 555,
        "nickname": "wxname",
        "ext": "null"
      }
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def get_token(uname,password):
    url = "https://data.singlocloud.com/login/login"

    payload = json.dumps({
      "username": uname,
      "password": password
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

    #print(response.text)
    Jsondata = response.text
    Jsondata = json.loads(Jsondata)##字符串转为字典
    return {'token':Jsondata['token'],'usercode':Jsondata['usercode']}


def get_payback(Token,uname):
    #95计费的
    url = "https://data.singlocloud.com/miner_v2/his_bill/2023"

    payload = {}
    headers = {
      'X-SL-Token': Token,
      'X-SL-User': uname
    }

    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

    print(response.text)
    Jsondata = response.text
    Jsondata = json.loads(Jsondata)##字符串转为字典
    return [Jsondata['data'][0]['bill_month'] ,Jsondata['data'][0]['bill_money']]
def get_xl(Token ,uname):
    #星L
    url = "https://data.singlocloud.com/miner_v2/v2/bill"
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    print(yesterday)
    payload = json.dumps({
      "begin_time":str(yesterday),
      "end_time":str(yesterday)
    })
    headers = {
      'X-SL-Token':Token,
      'X-SL-User':uname,
      'Content-Type':'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

    print(response.text)   
    Jsondata = response.text
    Jsondata = json.loads(Jsondata)##字符串转为字典
    return Jsondata['data']

def set_cookie():
    url = "https://portal.niulinkcloud.com/api/gaea/private/signin"

    payload = json.dumps({
      "mobile": "13800001234",##账号
      "password": "123456789",#密码
      "type": 1
    })

    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    # 获取cookie
    cookies = response.cookies
    print(response)
    # 打印cookie
    for cookie in cookies:
        print('0000')
        #print(cookie.name, cookie.value)
        return(cookie.value)
       # print(response.text)
def get_qiniu():
# 获取当前日期和时间
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    #set_cookie()
    #print(month)
    url = f"https://portal.niulinkcloud.com/api/proxy/jarvisbilling/v2/portal/48/month/bill?month=2023-0{month}&pointType=normal"

    payload = {}
    headers = {
      'cookie': f'LINKCLOUD_PORTAL_SESSION={set_cookie()}'
    }
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    print(yesterday)
    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)
    Jsondata = json.loads(response.text)##字符串转为字典
    print(Jsondata)
    for fruit in Jsondata['days']:
        #print(fruit['day'])
        if fruit['day']==str(yesterday):
            print(fruit['amount'])
            return str(fruit['amount'])
    #print(Jsondata['days'])


tokeninfo = get_token('账号','密码') #获取token ，写自己星L的用户名和密码
jinger1 = get_xl(tokeninfo['token'],tokeninfo['usercode']) #获取收益信息



def days_in_current_month():
    now = datetime.datetime.now()
    return calendar.monthrange(now.year, now.month)[1]

# 使用方法，判断当前月有多少天：
print(days_in_current_month())

print(jinger1[0])

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

RevenueInformation = '星L'+str(yesterday)+'收益'+str(jinger1[0])+'元'+'\n七N'+str(yesterday)+'收益'+get_qiniu()+'元'
print(RevenueInformation)
sendWx(RevenueInformation)##wxbot发送信息

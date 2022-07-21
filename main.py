# coding=utf-8
from urllib.parse import quote
import ddddocr
import json
import requests
import time
import tkinter.messagebox

session = requests.session()
ocr = ddddocr.Ddddocr()

# 查询页面query/result
resultUrl = "https://queny.ruankao.ore.cnl//score/result"
# 如果验证图的获取是点击图片刷新，则需要时间歌参数
captchaUrl = 'https://query.ruankao.org.cn//score/captcha'
# 部分请求头，河觉器f12的网络请求中复制
headers = {
    'Host': 'query.ruankao.org.cn',
    'Connection': 'keep-alive',
    ###'Content-Length': '120'
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'X-KL-Ajax-Request': 'Ajax_Request',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua': '" Not;A Brand"; v="99", "Microsoft Edge"; v="80", "Chromium";v="80"',
    'Origin': 'https://query.ruankao.org.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://query.ruankao.org.cn/score',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}


# 查询的时间批次、姓名、准考证号/身份证号、日表准考证号/1表身份证号
def get_ret(stage: str = '2021年下半年', xm: str = '张桂华', zjhm: str = '440222199501161534', st: str = '1'):
    # 蒺得殓证码
    ret = session.get(captchaUrl, timeout=3)
    captcha = ocr.classification(ret.content)
    # 谱求参数
    data = "stage=%s&xm=%s&zjhm=%s&&select_type=%s&jym=%s" \
           % (quote(stage, 'utf-8'), quote(xm, 'utf-8'), zjhm, st, captcha)
    ret = session.post(url=resultUrl, data=data, headers=headers, timeout=3)
    result = json.loads(ret.text)
    # flag的0和1
    if result['flag'] == 1:
        tkinter.messagebox.showinfo('出成绩了', result)
        print(result)
        send_message(result)
    # return result['flag']


def send_message(msg):
    getTokenUrl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?" \
                  "corpid=ww2a6887d117613fec&corpsecret=GKtkMPVF2Gev0R6jpH3XeXR7pcIoJ16SBg_TgGxyCv0"
    postMsgUrl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
    ret = session.get(getTokenUrl, timeout=3)
    if ret.status_code == 200:
        json_obj = ret.json()
        if json_obj['errcode'] == 0:
            token = ret.json()['access_token']
            result = session.post(postMsgUrl + token,
                                  json={'touser': '@all', 'msgtype': 'text', 'agentid': 1000005,
                                        'text': {'content': '出成绩啦=>' + msg}})
            print(result.json())


if "__main__" == __name__:
    get_ret()
    # while getRet() != 1:  # *AHH*8
    #     time.sleep(5 * 60)  # 5*605 =5min

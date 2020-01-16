from django.shortcuts import render
import requests
import re
import json
import execjs

def index_view(request):
    if request.method == 'GET':
        return render(request,'index.html')
    elif request.method == 'POST':
        token_url = 'https://fanyi.baidu.com'
        post_url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        headers =  {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'cookie': 'BIDUPSID=CF684F18FBB27AB6F9EB65F31EB5E7B6; PSTM=1574165062; BAIDUID=CF684F18FBB27AB6C57C94E7DEC0EB50:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; H_PS_PSSID=1461_21090_30210_30283; PSINO=6; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_2_2=1; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1576650124,1576650168,1576654434; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1576654434; __yjsv5_shitong=1.0_7_726171f465c12fc7e7635903e7fbcd129ff2_300_1576654434965_27.19.56.112_7f18d064; yjs_js_security_passport=f63fb4f05025274ca41dd7da868a1a8f58fee767_1576654466_js',
            'pragma': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        index_html = requests.get(url=token_url, headers=headers).text
        gtk = re.findall("window.gtk = '(.*?)'", index_html, re.S)[0]
        token = re.findall("token: '(.*?)'", index_html, re.S)[0]
        with open('translate.js','r') as f:
            data = f.read()
        ex = execjs.compile(data)
        word = request.POST.get('word')
        sign = ex.eval('e("{}","{}")'.format(word, gtk))
        if request.POST.get('type')=='汉译英':
            data = {'from': 'zh',
                    'to': 'en',
                    'query': word,
                    'transtype': 'realtime',
                    'simple_means_flag': '3',
                    'sign': sign,
                    'token': token}
            r_html = requests.post(url=post_url, data=data, headers=headers).json()
            result = r_html['trans_result']['data'][0]['dst']
            return render(request,'index.html',locals())
        if request.POST.get('type') == '英译汉':
            data = {'from': 'en',
                    'to': 'zh',
                    'query': word,
                    'transtype': 'realtime',
                    'simple_means_flag': '3',
                    'sign': sign,
                    'token': token}
            r_html = requests.post(url=post_url, data=data, headers=headers).json()
            result = r_html['trans_result']['data'][0]['dst']
            return render(request, 'index.html', locals())


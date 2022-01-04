import requests as rts
import pendulum
from pathlib import Path

systime = pendulum.now()
cst = systime.in_timezone('Asia/Shanghai')
filename = str(cst)[:10]+str(cst)[10:13]+str(cst)[14:16]
foldername = str(cst.date())

if not Path(foldername).exists():
    Path(foldername).mkdir()
    
def get_response(data):
    res = rts.post('https://kdkd.sizhu.tech/api/warn/changeRoom/',
                   headers={'Content-Type': 'application/json;charset=UTF-8'},
                   data=data)
    return res.json()


with open(Path(foldername)/(filename+'.csv'), 'a') as f:
    for i in range(1):
        BUILD = '研2' # ['研3', '梅1']
        ROOM = '6202'
        data = ('{"room":"'+BUILD+ROOM+'"}').encode('utf-8')
        res_ =  get_response(data)
        if res_['code'] == 200:
            res_data = res_['data']
            print(res_data['room'],
                  res_data['allAmp'],
                  res_data['usedAmp'],
                  res_data['updateAt'],
                  file=f, sep=',')

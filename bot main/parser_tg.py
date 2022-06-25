import asyncio
from datetime import datetime
import requests as req
from fake_useragent import UserAgent

from bot_dispatcher import bot

from datetime import datetime

ua = UserAgent()
user_agent = ua.random


url2 = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
headers = {
    'user-agent': user_agent,
}

p2p_status = False
async def set_parse_p2p_status(arg='check'):
    global p2p_status
    if arg == 'on':
        p2p_status = True
        return
    if arg == 'off':
        p2p_status = False
        return


async def p2p_func(chat_id, p2p_values):
    global p2p_status
    
    asset = p2p_values.get('asset')
    fiat = p2p_values.get('fiat')
    paytype = p2p_values.get('paytype')
    maxmin = p2p_values.get('maxmin')
    limit = p2p_values.get('limit')
    time_limit = p2p_values.get('time_limit')

    data = {
        "page": 1,
        "rows": 10,
        "payTypes": [paytype],
        "countries": [],
        "publisherType": None,
        "asset": asset,
        "fiat": fiat,
        "tradeType": "BUY"}
    print('-------------------P2P-STARTED----------------')
    print(data)
    viewed_orders = set()
    count = 0
    while True:
        if not p2p_status:
            return
        res_dict = {}
        
        response = req.post(url2, headers=headers, json=data)
        print('Request...')
        json_res = response.json()
        

        for obj in json_res.get('data')[:limit]:
            count += 1
            print('Successful Request')
            low = int(obj['adv']["minSingleTransAmount"].split('.')[0])
            max = int(obj['adv']["dynamicMaxSingleTransAmount"].split('.')[0])
            adv_id = obj['adv']["advNo"]
            print(f'----------------------OBJ {count}-----------------------------')
            print(low, max, adv_id, datetime.now())
            print('----------------------END-OBJ--------------------------------')
            # if low >= maxmin[0] and max <= maxmin[1]:
            if low <= maxmin and max >= maxmin:
                if adv_id in viewed_orders:
                    continue
                res_dict = {
                    'username': obj['advertiser']["nickName"],
                    'low_limit': low,
                    'max_limit': max,
                    'asset': obj['adv']["asset"],
                    'fiat': obj['adv']["fiatUnit"],
                    'price': obj['adv']["price"],
                    'assetAmount': obj['adv']["surplusAmount"],
                    'paytypename': [method['tradeMethodName'] for method in obj['adv']['tradeMethods']],
                }
                viewed_orders.add(adv_id)
                break
            res_dict = {}

        if res_dict:
            text = (f'''\
<b>{res_dict["username"]}</b> продаёт {res_dict["assetAmount"]} {res_dict["asset"]}\n\
<b>Лимит:</b> ({res_dict["low_limit"]}-{res_dict["max_limit"]} {res_dict["fiat"]})\n\
<b>Цена:</b> {res_dict["price"]} {res_dict["fiat"]}\n\
<b>Банк:</b> {res_dict["paytypename"]}\n\
<b>Ссылка:</b> https://p2p.binance.com/ru/trade/{paytype}/{asset}?fiat={fiat}\n\
''')
            await bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)

        await asyncio.sleep(time_limit)


# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from docs.conf import proxies
from common.Utils import timestamp_to_milliseconds

import logging
logger = logging.getLogger('main.haribo.luffy.ohlc.huobi')

def get_huobi_kline_json(symbol):
    url = 'https://api.huobipro.com/market/history/kline'
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    params = {'symbol': symbol,
              'period': '1min',
              'size': 1000}

    from urllib import parse
    postdata = parse.urlencode(params)

    try:
        import requests
        req = requests.get(url, postdata, headers=headers, proxies=proxies, timeout=5)

        if req.status_code == 200:
            return req.text
        else:
            return req.status_code
    except Exception as ex:
        logger.error('get_huobi_kline_json error ex:%s, url:%s' % (ex, url))
    return None


def parse_huobi_kline_json_to_influx_data(text, base, quote):
    import json

    json_arr = []
    try:
        response_arr = json.loads(text)['data']

        for response in response_arr:
            time = timestamp_to_milliseconds(int(response.get('id')))
            open = float(response.get('open'))
            close = float(response.get('close'))
            low = float(response.get('low'))
            high = float(response.get('high'))
            # amount = response.get('amount')
            # count = response.get('count')
            # vol = response.get('vol')

            json_body = 'kline_tb,market=huobi,base=%s,quote=%s open=%f,high=%f,low=%f,close=%f %d' \
                        % (base, quote, open, high, low, close, time)
            json_arr.append(json_body)
    except Exception as ex:
        logger.error('parse_huobi_kline_json_to_influx_data error, ex:' % ex)

    return json_arr


if __name__ == '__main__':
    pass
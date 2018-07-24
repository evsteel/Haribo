# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from docs.conf import proxies
from common.Utils import timestamp_to_milliseconds

import logging
logger = logging.getLogger('main.haribo.luffy.ohlc.okex')


def get_okex_kline_json(symbol):
    url = 'https://www.okex.com/api/v1/kline.do?size=2000&type=1min&symbol=%s' % symbol
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}

    try:
        import requests
        req = requests.get(url, proxies=proxies)

        if req.status_code == 200:
            return req.text
        else:
            return req.status_code
    except Exception as ex:
        logger.error('get_okex_kline_json error ex:%s ,url:%s' % (ex, url))
    return None


def parse_okex_kline_json_to_influx_data(text, base, quote):

    json_arr = []

    try:
        import json
        data_array = json.loads(text)
        for data in data_array:
            time = timestamp_to_milliseconds(int(data[0]))
            open = float(data[1])
            high = float(data[2])
            low = float(data[3])
            close = float(data[4])
            # volume = float(data[5])

            json_body = "kline_tb,market=okex,base=%s,quote=%s open=%f,high=%f,low=%f,close=%f %d" \
                        % (base, quote, open, high, low, close, time)
            json_arr.append(json_body)
    except Exception as ex:
        logger.error('parse_okex_kline_json_to_influx_data error, ex:' % ex)
    return json_arr


if __name__ == '__main__':
    pass
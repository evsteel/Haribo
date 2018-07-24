# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from docs.conf import proxies
from common.Utils import timestamp_to_milliseconds

import logging
logger = logging.getLogger('main.haribo.luffy.ohlc.gdax')


def get_gdax_kline_json(symbol):

    url = "https://api.gdax.com/products/%s/candles" % symbol
    try:
        import requests
        req = requests.get(url)

        if req.status_code == 200:
            return req.text
        else:
            return req.status_code
    except Exception as ex:
        logger.error('get_gdax_klien_json error ex:%s ,url:%s' % (ex, url))
    return None


def parse_gdax_kline_json_to_influx_data(text, base, quote):

    json_arr = []

    try:
        import json
        data_array = json.loads(text)

        for data in data_array:

            time = timestamp_to_milliseconds(int(data[0]))

            low = float(data[1])
            high = float(data[2])
            open = float(data[3])
            close = float(data[4])
            # volume = float(data[5])
            json_body = 'kline_tb,market=gdax,base=%s,quote=%s open=%f,high=%f,low=%f,close=%f %d' \
                        % (base, quote, open, high, low, close, time)
            json_arr.append(json_body)
    except Exception as ex:
        logger.error('parse_gdax_kline_json_to_influx_data error, ex:' % ex)

    return json_arr


if __name__ == "__main__":
    pass


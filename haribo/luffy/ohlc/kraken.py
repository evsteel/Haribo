# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from docs.conf import proxies
from common.Utils import timestamp_to_milliseconds

import logging
logger = logging.getLogger('main.haribo.luffy.ohlc.kraken')


def get_kraken_kline_json(symbol):
    import requests

    url = 'https://api.kraken.com/0/public/OHLC?interval=%d&pair=%s' % (1, symbol)
    try:
        req = requests.get(url)

        if req.status_code == 200:
            return req.text
        else:
            return req.status_code
    except Exception as ex:
        logger.error('get_kraken_kline_json error ex:%s ,url:%s' % (ex, url))
    return None


def parse_kraken_kline_json_to_influx_data(text, base, quote):

    json_arr = []

    try:
        import json
        result_dict = json.loads(text)['result']
        for key in result_dict.keys():
            if key != 'last':
                ohlc_array = result_dict[key]
                for ohlc_data in ohlc_array:

                    time = timestamp_to_milliseconds(int(ohlc_data[0]))

                    open = float(ohlc_data[1])
                    high = float(ohlc_data[2])
                    low = float(ohlc_data[3])
                    close = float(ohlc_data[4])
                    # vwap = float(ohlc_data[5])
                    # volume = float(ohlc_data[6])
                    # count = int(ohlc_data[7])

                    json_body = 'kline_tb,market=kraken,base=%s,quote=%s open=%f,high=%f,low=%f,close=%f %d' \
                                % (base, quote, open, high, low, close, time)
                    json_arr.append(json_body)
    except Exception as ex:
        logger.error('parse_kraken_kline_json_to_influx_data error, ex:' % ex)

    return json_arr


if __name__ == '__main__':
    pass


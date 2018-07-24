# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from docs.conf import proxies
from common.Utils import timestamp_to_milliseconds

import logging
logger = logging.getLogger('main.haribo.luffy.ohlc.binance')


def get_binance_kline_json(symbol):

    url = 'https://api.binance.com/api/v1/klines?&limit=500&interval=1m&symbol=%s' % symbol

    try:
        import requests
        req = requests.get(url, proxies=proxies)

        if req.status_code == 200:
            return req.text
        else:
            return req.status_code
    except Exception as ex:
        logger.error('get_binance_klien_update_sql error ex:%s ,url:%s' % (ex, url))
    return None


def parse_binance_kline_json_to_influx_data(text, base, quote):
    import json

    json_arr = []

    try:
        response_arr = json.loads(text)
        for response in response_arr:
            time = timestamp_to_milliseconds(int(response[0]))
            open = float(response[1])
            high = float(response[2])
            low = float(response[3])
            close = float(response[4])
            # volume = float(response[5])
            # close_time = int(response[6])
            # quote_asset_vol = float(response[7])
            # count = int(response[8])
            # taker_buy_base_asset_vol = float(response[9])
            # taker_buy_quote_asset_vol = float(response[10])

            json_body = 'kline_tb,market=binance,base=%s,quote=%s' \
                        ' open=%f,high=%f,low=%f,close=%f %d' \
                        % (base, quote, open, high, low, close, time)
            json_arr.append(json_body)
    except Exception as ex:
        logger.error('parse_binance_kline_json_to_influx_data error, ex:' % ex)

    return json_arr


if __name__ == "__main__":
    pass
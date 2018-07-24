import sys
sys.path.append("..")

from common.Utils import InfluxDBConnector
from docs.conf import market_symbols_dict, proxy_url, proxy_port

import logging
logger = logging.getLogger('main.haribo.luffy.ticker.binance')

try:
    import thread
except ImportError:
    import _thread as thread


import json


from websocket import create_connection, WebSocketApp

WSS_URL = 'wss://stream.binance.com:9443'
DATABASE_BASE_URL = 'http://localhost:8086/'


def send_influx_request(endpoint, data=''):
    import requests
    res = requests.post('%s%s' % (DATABASE_BASE_URL, endpoint), data=data)
    return res


class binance_depth(object):
    base = ''
    quote = ''
    stream = ''
    event_type = 'depthUpdate'
    event_time = 0
    symbol = ''
    first_update_id = 0
    final_update_id = 0
    bids_dict = {}
    asks_dict = {}

    def __init__(self):
        pass

    def parse_websocket_depth_feed(self, depth_feed_string):
        try:
            depth_feed_arr = json.loads(depth_feed_string)
            self.stream = depth_feed_arr['stream']
            self.event_type = depth_feed_arr['data']['e']
            self.event_time = int(depth_feed_arr['data']['E'])
            self.symbol = depth_feed_arr['data']['s']
            self.first_update_id = int(depth_feed_arr['data']['U'])
            self.final_update_id = int(depth_feed_arr['data']['u'])
            self.bids_dict = depth_feed_arr['data']['b'] 
            self.asks_dict = depth_feed_arr['data'] ['a']
            pair = self.stream.split('@')[0].upper()
            self.base = market_symbols_dict['binance'][pair]['base']
            self.quote = market_symbols_dict['binance'][pair]['quote']
        except Exception as ex:
            logger.error('[ERROR]parse websocket depth feed error! ex:%s' % ex)
            return False
        return True

    def get_influx_string(self):
        influx_sql_arr = []
        for bid in self.bids_dict:
            influx_sql_arr.append('depth_feed_tb,market=binance,base=%s,quote=%s,action=bid time=%d,price=%f,quantity=%f'
                                    % (self.base, self.quote, self.event_time, float(bid[0]), float(bid[1])))
        for ask in self.asks_dict:
            influx_sql_arr.append('depth_feed_tb,market=binance,base=%s,quote=%s,action=ask time=%d,price=%f,quantity=%f'
                                    % (self.base, self.quote, self.event_time, float(ask[0]), float(ask[1])))        
        return influx_sql_arr


class binance_trade(object):
    base = ''
    quote = ''
    stream = ''
    event_type = "trade"
    event_time = 0
    symbol = ""
    trade_id = 0
    price = 0.0
    quantity = 0.0
    buyer_order_id = 0
    seller_order_id = 0
    trade_time = 0
    is_buyer_market_maker = False

    def __init__(self):
        pass

    def parse_websocket_trade_feed(self, trade_feed_string):
        try:
            trade_feed_arr = json.loads(trade_feed_string)
            self.stream = trade_feed_arr['stream']
            self.event_type = trade_feed_arr['data'].get('e')
            self.event_time = int(trade_feed_arr['data'].get('E'))
            self.symbol = trade_feed_arr['data'].get('s')
            self.trade_id = int(trade_feed_arr['data'].get('t'))
            self.price = float(trade_feed_arr['data'].get('p'))
            self.quantity = float(trade_feed_arr['data'].get('q'))
            self.buyer_order_id = int(trade_feed_arr['data'].get('b'))
            self.seller_order_id = int(trade_feed_arr['data'].get('a'))
            self.trade_time = int(trade_feed_arr['data'].get('T'))
            self.is_buyer_market_maker = trade_feed_arr['data'].get('m')
            pair = self.stream.split('@')[0].upper()
            self.base = market_symbols_dict['binance'][pair]['base']
            self.quote = market_symbols_dict['binance'][pair]['quote']
        except Exception as ex:
            logger.error('[ERROR]parse websocket trade feed error! ex:%s' % ex)
            return False
        return True

    def get_influx_string(self):
        influx_sql_str = 'trade_feed_tb,market=binance,base=%s,quote=%s ' \
                         'stream="%s",event_type="%s",event_time=%d,symbol="%s",trade_id=%d,price=%f,quantity=%f,buyer_order_id=%d,seller_order_id=%d,trade_time=%d,is_buyer_market_maker=%d' \
                         % (self.base, self.quote, self.stream, self.event_type, self.event_time, self.symbol, self.trade_id, self.price, self.quantity, self.buyer_order_id, self.seller_order_id, self.trade_time, self.is_buyer_market_maker)
        return influx_sql_str


def on_message(ws, message):
    influx_client = InfluxDBConnector()
    logger.debug(message.replace('\n', ''))
    recv_feed_dict = json.loads(message)
    stream_str = recv_feed_dict['stream']
    if stream_str.find('depth') > 0:
        binance_depth_obj = binance_depth()
        binance_depth_obj.parse_websocket_depth_feed(message)
        data_str = binance_depth_obj.get_influx_string()
        for depth_str in binance_depth_obj.get_influx_string():
            influx_client.insert(depth_str)
    elif stream_str.find('trade') > 0:
        binance_trade_obj = binance_trade()
        binance_trade_obj.parse_websocket_trade_feed(message)
        data_str = binance_trade_obj.get_influx_string()
        database_response_code = send_influx_request(endpoint='write?db=cryptocurrency_db&precision=ms', data=data_str)


def on_error(ws, error):
    logger.error("System error, err message:%s" % error)


def on_close(ws):
    logger.info('Socket closed.')
    ws.close()


def on_open(ws):
    logger.info('Socket open.')


def main():
    streamlist = list()
    streamlist.append('btcusdt@depth')
    streamlist.append('btcusdt@trade')
    if len(streamlist) > 1:
        stream_string = '/stream?streams='
        for stream in streamlist:
            stream_string = '%s%s/' % (stream_string, stream)
    else:
        stream_string = '/ws/%s' % streamlist[0]

    ws = WebSocketApp('%s%s' % (WSS_URL, stream_string), on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    while True:
        ws.run_forever(http_proxy_host=proxy_url, http_proxy_port=proxy_port)


def init_database():
    database_resposne_code = send_influx_request(endpoint='query', data={"q":"CREATE DATABASE binance_feed"})


def main_loop():
    init_database()
    main()


if __name__ == '__main__':
    main_loop()
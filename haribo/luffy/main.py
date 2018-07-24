import threading
from threading import Timer

import sys
sys.path.append('..')
from docs.conf import market_symbols_dict, market_symbols_max_interval
from common.Utils import InfluxDBConnector
from binance import parse_binance_kline_json_to_influx_data, get_binance_kline_json
from huobi import parse_huobi_kline_json_to_influx_data, get_huobi_kline_json
from kraken import parse_kraken_kline_json_to_influx_data, get_kraken_kline_json
from okex import parse_okex_kline_json_to_influx_data, get_okex_kline_json
from gdax import parse_gdax_kline_json_to_influx_data, get_gdax_kline_json

import logging
logger = logging.getLogger('main.haribo.main')


def update_kline_loop(market, symbol, loop_interval):
    logger.info('update_kline_loop awake, market:%s, symbol:%s, loop_gap:%f' % (market, symbol, loop_interval))
    base = market_symbols_dict[market][symbol]['base']
    quote = market_symbols_dict[market][symbol]['quote']
    response_text = eval('get_%s_kline_json' % market)(symbol)
    json_arr = eval('parse_%s_kline_json_to_influx_data' % market)(response_text, base, quote)
    influx_client = InfluxDBConnector()
    logger.info('update_kline_loop insert result: %s' % influx_client.insertMultiple(json_arr))
    influx_client.close()
    logger.info('update_kline_loop finish, market:%s, symbol:%s' % (market, symbol))
    register_timer(market, symbol, loop_interval)


def register_timer(market, symbol, loop_interval):
    logger.info("register_time market:%s, symbol:%s, loop_interval:%f"
          % (market, symbol, loop_interval))
    Timer(interval=loop_interval,
          function=update_kline_loop,
          args=[market, symbol, loop_interval, ]).start()


def kline_loop():
    logger.info('Kline loop called')
    for market in market_symbols_dict.keys():
        current_market_interval = market_symbols_max_interval[market] \
                             / len(market_symbols_dict[market])
        current_timer_interval = 0

        for symbol in market_symbols_dict[market].keys():
            logger.info('Kline loop register service, market:%s, symbol:%s, interval:%f, current_market_gap:%f'
                  % (market, symbol, current_timer_interval, current_market_interval))
            Timer(interval=current_timer_interval,
                  function=update_kline_loop,
                  args=[market, symbol, market_symbols_max_interval[market]]).start()
            current_timer_interval += current_market_interval


def ticker_loop():
    import ticker.binance
    ticker.binance.main()


def main_loop():
    t = threading.Thread(target=kline_loop)
    t.start()

    t = threading.Thread(target=ticker_loop)
    t.start()

if __name__ == "__main__":
    main_loop()
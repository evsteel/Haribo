# influxDB settings
## login settings
influxDB_conf = {'ip': '127.0.0.1',
                 'port': 8086,
                 'username': 'root',
                 'password': 'root',
                 'url': 'http://127.0.0.1:8086'}
## Project's DB name
DB_NAME = "cryptocurrency_db"
## OHLC table name
TB_NAME = 'ohlc_tb'


# Luffy settings
## Proxy settings
proxy_url = '127.0.0.1'
proxy_port = '1080'
proxies = {'http': 'http://%s:%s' % (proxy_url, proxy_port), 'https': 'http://%s:%s' % (proxy_url, proxy_port)}
## Each market max query interval settings
market_symbols_max_interval = \
    {
        'binance': 24000,
        'huobi': 48000,
        'kraken': 36000,
        'okex': 96000,
        'gdax': 15000
    }
## Market Symbol settings
market_symbols_dict = \
{
    'huobi':
        {'btcusdt': {"base": "BTC", "quote": "USDT"},
         'ethbtc': {"base": "ETH", "quote": "BTC"},
         'etcbtc': {"base": "ETC", "quote": "BTC"},
         'ltcbtc': {"base": "LTC", "quote": "BTC"},
         'bchbtc': {"base": "BCH", "quote": "BTC"},
         'ethusdt': {"base": "ETH", "quote": "USDT"},
         'etcusdt': {"base": "ETC", "quote": "USDT"},
         'ltcusdt': {"base": "LTC", "quote": "USDT"},
         'bchusdt': {"base": "BCH", "quote": "USDT"},
         'htusdt': {"base": "HT", "quote": "USDT"},
         'htbtc': {"base": "HT", "quote": "BTC"},
         "hteth": {"base": "HT", "quote": "ETH"}},
    'okex':
        {'btc_usdt': {"base": "BTC", "quote": "USDT"},
         'etc_usdt': {"base": "ETC", "quote": "USDT"},
         'eth_usdt': {"base": "ETH", "quote": "USDT"},
         'bch_usdt': {"base": "BCH", "quote": "USDT"},
         'ltc_usdt': {"base": "LTC", "quote": "USDT"},
         'eth_btc': {"base": "ETH", "quote": "BTC"},
         'etc_btc': {"base": "ETC", "quote": "BTC"},
         'ltc_btc': {"base": "LTC", "quote": "BTC"},
         'bch_btc': {"base": "BCH", "quote": "BTC"},
         'etc_eth': {"base": "ETH", "quote": "ETC"}},
    'binance':
        {'BTCUSDT': {"base": "BTC", "quote": "USDT"},
         'ETHUSDT': {"base": "ETH", "quote": "USDT"},
         'LTCUSDT': {"base": "LTC", "quote": "USDT"},
         'BCCUSDT': {"base": "BCH", "quote": "USDT"},
         'ETHBTC': {"base": "ETH", "quote": "BTC"},
         'ETCBTC': {"base": "ETC", "quote": "BTC"},
         'LTCBTC': {"base": "LTC", "quote": "BTC"},
         'BCCBTC': {"base": "BCH", "quote": "BTC"},
         'ETCETH': {"base": "ETC", "quote": "ETH"},
         'LTCETH': {"base": "LTC", "quote": "ETH"},
         'BCCETH': {"base": "BCC", "quote": "ETH"}},
    'gdax':
        {'BTC-USD': {"base": "BTC", "quote": "USD"},
         'ETH-USD': {"base": "ETH", "quote": "USD"},
         'LTC-USD': {"base": "LTC", "quote": "USD"},
         'BCH-USD': {"base": "BCH", "quote": "USD"},
         'ETH-BTC': {"base": "ETH", "quote": "BTC"},
         'LTC-BTC': {"base": "LTC", "quote": "BTC"},
         'BCH-BTC': {"base": "BCH", "quote": "BTC"}},
    'kraken':
        {'USDTUSD': {"base": "USDT", "quote": "USD"},
         'XBTUSD': {"base": "BTC", "quote": "USD"},
         'ETHUSD': {"base": "ETH", "quote": "USD"},
         'ETCUSD': {"base": "ETC", "quote": "USD"},
         'LTCUSD': {"base": "LTC", "quote": "USD"},
         'BCHUSD': {"base": "BCH", "quote": "USD"},
         'ETHXBT': {"base": "ETH", "quote": "BTC"},
         'ETCXBT': {"base": "ETC", "quote": "BTC"},
         'LTCXBT': {"base": "LTC", "quote": "BTC"},
         'BCHXBT': {"base": "BCH", "quote": "BTC"}},
}
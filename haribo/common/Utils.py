import sys
sys.path.append('..')

from docs.conf import influxDB_conf, DB_NAME, market_symbols_dict


class InfluxDBConnector:

    def __init__(self):
        pass

    def close(self):
        pass

    def insert(self, sql_str, precision='ms'):
        import requests

        headers = {}

        res = requests.post('%s/write?db=%s&precision=%s' % (influxDB_conf['url'], DB_NAME, precision),
                            headers=headers,
                            data=sql_str)
        return str(res.status_code)

    def insertMultiple(self, sql_arr, precision='ms'):
        import requests

        headers = {"content-type": "text/plain; charset=UTF-8"}
        sql_str = '\n'.join(sql_arr)
        # print(sql_str)
        res = requests.post('%s/write?db=%s&precision=%s' % (influxDB_conf['url'], DB_NAME, precision),
                            headers=headers,
                            data=sql_str)
        return str(res.status_code)

    def multi_insert(self, data_str):
        pass

    def query(self, sql_str, precision='ms'):
        import requests

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = 'db=%s&epoch=%s&q=%s' % (DB_NAME, precision, sql_str)

        res = requests.post('%s/query' % influxDB_conf['url'], headers=headers, data=payload)
        return res.text


def get_symbol_base_quote(self, market, symbol):
    base = market_symbols_dict[market][symbol]['base']
    quote = market_symbols_dict[market][symbol]['quote']
    returnDict = {'base': base, 'quote': quote}
    return returnDict


def timestamp_to_milliseconds(timestamp):
    while timestamp < 999999999999:
        timestamp = timestamp * 10
    return timestamp
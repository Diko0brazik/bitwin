import requests
import json
import time
import base64
import hmac
import hashlib


PROTOCOL = "https"
HOST = "api.bitfinex.com"
VERSION = "v1"

PATH_SYMBOLS = "symbols"
PATH_TICKER = "ticker/%s"
PATH_TODAY = "today/%s"
PATH_STATS = "stats/%s"
PATH_LENDBOOK = "lendbook/%s"
PATH_ORDERBOOK = "book/%s"
TIMEOUT = 5.0


class BitfinexClient: #Клиент для работы с Битфайнексом

    def __init__(self, key = float('nan'), secret = float('nan')):
        if key != key:
            key, secret = self._readfromfile()
        self.URL = "{}://{}/{}".format(PROTOCOL, HOST, VERSION)
        self.URL_POST = "{0:s}://{1:s}".format(PROTOCOL, HOST)
        self.KEY = key
        self.SECRET = secret
        pass

    def _server(self):
        return u"{0:s}://{1:s}/{2:s}".format(PROTOCOL, HOST, VERSION)

    def _convert_to_floats(self, data):
        """
        Convert all values in a dict to floats
        """
        for key, value in data.items():
            data[key] = float(value)
        return data

    def _url_for(self, path, path_arg=None, parameters=None):
        # build the basic url
        url = "%s/%s" % (self._server(), path)

        # If there is a path_arh, interpolate it into the URL.
        # In this case the path that was provided will need to have string
        # interpolation characters in it, such as PATH_TICKER
        if path_arg:
            url = url % (path_arg)

        # Append any parameters to the URL.
        if parameters:
            url = "%s?%s" % (url, self._build_parameters(parameters))
        return url

    def _readfromfile(self):
        with open('keybitfinex.txt') as f:
            data = f.read().splitlines()
        print(data)
        return data

    def _get(self, url):
        return requests.get(url, timeout=TIMEOUT).json()

    def _post(self, url):
        payload = {
            "request": url,
            "nonce": self._nonce
        }

        signed_payload = self._sign_payload(payload)
        url = self.URL_POST + url
        r = requests.post(url, headers=signed_payload, verify=True)
        json_resp = r.json()
        return json_resp

    @property
    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(time.time() * 1000000)

    def _sign_payload(self, payload):
        j = json.dumps(payload)
        data = base64.standard_b64encode(j.encode('utf8'))

        h = hmac.new(self.SECRET.encode('utf8'), data, hashlib.sha384)
        signature = h.hexdigest()
        return {
            "X-BFX-APIKEY": self.KEY,
            "X-BFX-SIGNATURE": signature,
            "X-BFX-PAYLOAD": data
        }

    def ticker(self, symbol):
        """
        GET /ticker/:symbol
        curl https://api.bitfinex.com/v1/ticker/btcusd
        {
            'ask': '562.9999',
            'timestamp': '1395552290.70933607',
            'bid': '562.25',
            'last_price': u'562.25',
            'mid': u'562.62495'}
        """
        data = self._get(self._url_for(PATH_TICKER, (symbol)))

        # convert all values to floats
        return self._convert_to_floats(data)

    def active_orders(self):
        """
        Fetch active orders
        """

        json_resp = self._post('/v1/orders')
        return json_resp

    def balances(self):
        """
        Fetch balances

        :return:
        """
        json_resp = self._post("/v1/balances")
        return json_resp

    def getListOfExchangePositions(self):
        """
        List of not nul currencys
        :return:
        {'type': 'trading',
        'currency': 'btc',
        'amount': '0.0001106',
        'available': '0.0001106',
        'price': 6305.3}
        """
        balances = self.balances()
        notNulCurrencies = []
        for item in balances:
            if not float(item['amount']) == 0:
                notNulCurrencies.append(item)
        for item in notNulCurrencies:
            if item['currency'] == 'usd':
                item['price'] = 1
            else:
                price = self.ticker(item['currency'] + 'usd')
                item['price'] = price['last_price']
        return notNulCurrencies

    def getListOfMarginPositions(self):
        """
        Get list of margin positions
        :return:
        list of dict
        {'id': 138259326, 'symbol': 'ethbtc', 'status': 'ACTIVE', 'base': '0.04101', 'amount': '-0.1', 'timestamp': '1535849072.0', 'swap': '0.0', 'pl': '-0.0000083022'}
        """
        payload = {
            "request": "/v1/positions",
            "nonce": self._nonce
        }
        signed_payload = self._sign_payload(payload)
        r = requests.post(self.URL + "/positions", headers=signed_payload, verify=True)
        json_resp = r.json()
        for item in json_resp:
            item['price'] = self.ticker(item['symbol'])['last_price']
        return json_resp


#b = BitfinexClient()

#data = b.getListOfExchangePositions()

#print(data)

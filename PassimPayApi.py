import hmac
import requests
import json
import hashlib
from urllib.parse import urlencode

class PassimpayApi:
    URL_BASE = 'https://api.passimpay.io'

    def __init__(self, platform_id, secret_key):
        self.platform_id = platform_id
        self.secret_key = secret_key

    def _make_request(self, endpoint, data=None):
        if not self.secret_key:
            raise Exception('Passimpay: secret key can not be empty.')

        if not self.platform_id:
            raise Exception('Passimpay: platform id can not be empty.')

        url = f'{self.URL_BASE}/{endpoint}'
        payload = {'platform_id': self.platform_id}

        if data:
            payload.update(data)
        payload_str = urlencode(payload)
        #payload_str = "&".join(f"{key}={value}" for key, value in payload.items()).encode('utf-8')
        print(payload_str)
        #hash_value = hmac.new(self.secret_key.encode('utf-8'), payload_str, hashlib.sha256).hexdigest()
        hash_value = hmac.new(secret_key.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
        print('hash_value : ',hash_value)
        # data = {
        #     'platform_id': self.platform_id,
        #     'hash': hash_value,
        # }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = payload_str + f"&hash={hash_value}"
        print('data :',data)
        
        response = requests.post(url, data=data,headers=headers,verify=False)

        return response.json()

    def handle_error(self, error_message):
        if error_message:
            print(f'error: {error_message}')
            return True
        return False

    def check_and_print(self, result, error_message):
        if not self.handle_error(error_message):
            print(result)

    def balance(self):
        response = self._make_request('balance')
        balance, error = response.get('balance'), response.get('message')
        self.check_and_print(f'Баланс: {balance}', error)
        return balance, error

    def currencies(self):
        response = self._make_request('currencies')
        currencies, error = response.get('list'), response.get('message')
        self.check_and_print(f'Список доступных валют: {currencies}', error)
        return currencies, error

    def invoice(self, id, amount,currencies):
        data = {
            'order_id': id,
            'amount': amount,
            'currencies': currencies
        }
        response = self._make_request('createorder', data)
        url, error = response.get('url'), response.get('message')
        self.check_and_print(f'Invoice URL: {url}', error)
        return url, error

    def invoice_status(self, id):
        data = {'order_id': id}
        response = self._make_request('orderstatus', data)
        status, error = response.get('status'), response.get('message')
        self.check_and_print(f'Invoice Status: {status}', error)
        return status, error

    def payment_wallet(self, order_id, payment_id):
        data = {
            'payment_id': payment_id,
            'platform_id': self.platform_id,
            'order_id': order_id
        }
        response = self._make_request('getpaymentwallet', data)
        address, error = response.get('address'), response.get('message')
        self.check_and_print(f'Payment Wallet Address: {address}', error)
        return address, error

    def withdraw(self, payment_id, address_to, amount):
        data = {
            'payment_id': payment_id,
            'platform_id': self.platform_id,
            'amount': amount,
            'address_to': address_to
        }
        response = self._make_request('withdraw', data)
        self.check_and_print(f'Withdrawal Response: {response}', response.get('message'))
        return response, response.get('message')

    def transaction_status(self, tx_hash):
        data = {'txhash': tx_hash}
        response = self._make_request('transactionstatus', data)
        self.check_and_print(f'Transaction Status: {response}', response.get('message'))
        return response, response.get('message')


# Пример использования
platform_id = 775
currencies='10,20,30'
order_id = 2
amount='100.00'
secret_key = '846bd8-a8c82d-c2607e-41b229-f314b9'

passimpay_api = PassimpayApi(platform_id, secret_key)

# passimpay_api.balance()
# passimpay_api.currencies()

passimpay_api.invoice(order_id,amount,currencies)
# passimpay_api.invoice_status(order_id)

# order_id = 'your_order_id'
# payment_id = 'your_payment_id'
# passimpay_api.payment_wallet(order_id, payment_id)

# payment_id = 'your_payment_id'
# address_to = 'recipient_address'
# amount = 100.0
# passimpay_api.withdraw(payment_id, address_to, amount)

# tx_hash = 'your_transaction_hash'
# passimpay_api.transaction_status(tx_hash)
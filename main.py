# This is a sample Python script.
import os

import requests
import time

# global variables
API_KEY = os.getenv('API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('USER_ID')
threshold = 4000
summary_interval = 12
min_interval = 5
time_interval = min_interval * 60  # in seconds


def get_eth_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()
    # extract the bitcoin price from the json data
    btc_price = response_json['data'][1]
    return btc_price['quote']['USD']['price']


# fn to send_message through telegram
def send_message(chat_id, msg):
    print(f"Sending: {msg}, to {chat_id}")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    # send the msg
    requests.get(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    price_list = []
    last_price = 0.0
    # infinite loop
    while True:
        price = get_eth_price()
        price_list.append(price)
        # if the price falls below threshold, send an immediate msg
        if price < (last_price * .95):
            send_message(chat_id=CHAT_ID, msg=f'ETH >5% Drop: {price}')
        if price > (last_price * 1.05):
            send_message(chat_id=CHAT_ID, msg=f"ETH >5% Increase: {price}")
        # send last 6 btc price
        if len(price_list) >= summary_interval:
            price_change_pct = (price_list[0] - price_list[5]) / price_list[0] * 100
            send_message(chat_id=CHAT_ID, msg=f"ETH has changed {price_change_pct:.2f}% in last {summary_interval} intervals")
            send_message(chat_id=CHAT_ID, msg=f"Current price: {price:.4f}")
            # empty the price_list
            price_list = []
        # fetch the price for every dash minutes
        last_price = price
        time.sleep(time_interval)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

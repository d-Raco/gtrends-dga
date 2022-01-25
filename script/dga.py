import json
import requests
from requests.exceptions import ConnectionError
import pandas as pd
from pytrends.request import TrendReq
import datetime
import hashlib
import pytz

dictionary_filename = 'dict_common.json'
#dictionary_filename = 'dict_full.json'

seed = '0a5d7b1f194820e1377d9348ff98'


def generate_index(today, mod):
    string = seed + str(today.year + today.month + today.day + today.hour + mod)
    hash = hashlib.md5(string.encode()).hexdigest()

    return hash


def google_trends(mod):
    today = datetime.datetime.now(pytz.utc)

    pytrend = TrendReq()
    df = pytrend.trending_searches()
    trend = df[0][int(generate_index(today, mod), base = 16) % df.size] + str(today.year + today.month + today.day + today.hour + mod)

    hash = hashlib.md5(trend.encode()).hexdigest()

    return hash


def generate_domain(num):
    with open(dictionary_filename, "r") as r:
        dictionary = json.load(r)

    domain = ""

    for domain_component in ['adjective', 'separator', 'noun', 'tld']:
        dd = dictionary[domain_component]
        domain += dd[num % len(dd)]
    
    return domain


def check_domain(domain):
    try:
        response = requests.get(f'http://{domain}', timeout = 10)
    except ConnectionError:
        return False
    else:
        return True


if __name__ == "__main__":
    mod = 0

    domain = generate_domain(int(google_trends(mod), base = 16))

    # To search for available domain:
    # while not (check_domain(domain)):

    # To search for registered domain:
    while (check_domain(domain)):
        mod += 1
        domain = generate_domain(int(google_trends(mod), base = 16))

    print(domain)
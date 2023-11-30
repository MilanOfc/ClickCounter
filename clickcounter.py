import sys

import requests
import os
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

bitly_url_template = 'https://api-ssl.bitly.com/v4/'


def shorten_link(url, token):
    """
    return shortened link of url
    :param token: str
    :param url: str
    :return: short_link: str
    """
    payload = {'long_url': url}
    headers = {'Authorization': 'Bearer ' + token}
    bitly_url = urljoin(bitly_url_template, 'shorten')
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json().get('link')
    return bitlink


def count_clicks(bitlink, token):
    """
    return number of clicks on given url
    :param token: str
    :param url: str
    :return: clicks_amount: int
    """
    bitlink = urlparse(bitlink).netloc + urlparse(bitlink).path
    params = {'unit': 'month', 'units': -1}
    headers = {'Authorization': 'Bearer ' + token}
    bitly_url = urljoin(bitly_url_template, f'bitlinks/{bitlink}/clicks/summary')
    response = requests.get(bitly_url, headers=headers, params=params)
    response.raise_for_status()
    clicks_amount = response.json().get('total_clicks')
    return clicks_amount


def is_bitlink(url, token):
    """
    Check is this url bitlink or not
    :param token: str
    :param url: str
    :return: bool
    """
    url = urlparse(url).netloc + urlparse(url).path
    headers = {'Authorization': 'Bearer ' + token}
    bitly_url = urljoin(bitly_url_template, f'bitlinks/{url}')
    response = requests.get(bitly_url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    url = input('Please enter the link: ')
    if is_bitlink(url, bitly_token):
        print('Total clicks: ', count_clicks(url, bitly_token))
    else:
        try:
            shorten_link(url, bitly_token)
        except requests.exceptions.HTTPError:
            print('You entered wrong url, please try again')
            sys.exit()
        print('Bitlink: ', shorten_link(url, bitly_token))

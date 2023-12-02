import sys

import requests
import os
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

BITLY_URL_TEMPLATE = 'https://api-ssl.bitly.com/v4/'


def shorten_link(url, token):
    """
    return shortened link of url
    :param token: str
    :param url: str
    :return: short_link: str
    """
    payload = {'long_url': url}
    headers = {'Authorization': f'Bearer {token}'}
    bitly_url = urljoin(BITLY_URL_TEMPLATE, 'shorten')
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
    params = {'unit': 'month', 'units': -1}
    headers = {'Authorization': f'Bearer {token}'}
    bitly_url = urljoin(BITLY_URL_TEMPLATE, f'bitlinks/{bitlink}/clicks/summary')
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
    headers = {'Authorization': f'Bearer {token}'}
    bitly_url = urljoin(BITLY_URL_TEMPLATE, f'bitlinks/{url}')
    response = requests.get(bitly_url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    url = input('Please enter the link: ')
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}{parsed_url.path}'
    try:
        if is_bitlink(bitlink, bitly_token):
            count_clicks(bitlink, bitly_token)
            print('Total clicks: ', count_clicks(bitlink, bitly_token))
        else:
            shorten_link(url, bitly_token)
            print('Bitlink: ', shorten_link(url, bitly_token))
    except requests.exceptions.HTTPError:
        print('You entered wrong url, please try again')
        sys.exit()
import requests
import os
from urllib.parse import urljoin
from dotenv import load_dotenv


def remove_https(url: str):
    return url.replace('http://', '').replace('https://', '')


def shorten_link(url):
    """
    return shortened link of url
    :param token: str
    :param url: str
    :return: short_link: str
    """
    payload = {'long_url': url}
    bitly_url = urljoin(bitly_url_template, 'shorten')
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json().get('link')
    return bitlink


def count_clicks(bitlink):
    """
    return number of clicks on given url
    :param token: str
    :param url: str
    :return: clicks_amount: int
    """
    bitlink = remove_https(bitlink)
    params = {'unit': 'month', 'units': -1}
    bitly_url = urljoin(bitly_url_template, f'bitlinks/{bitlink}/clicks/summary')
    response = requests.get(bitly_url, headers=headers, params=params)
    response.raise_for_status()
    clicks_amount = response.json().get('total_clicks')
    return clicks_amount


def is_bitlink(url):
    """
    Check is this url bitlink or not
    :param token: str
    :param url: str
    :return: bool
    """
    url = remove_https(url)
    bitly_url = urljoin(bitly_url_template, f'bitlinks/{url}')
    response = requests.get(bitly_url, headers=headers)
    try:
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError:
        return False


def catch_exceptions(url, func):
    try:
        func(url)
        return False
    except requests.exceptions.HTTPError:
        return True


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['token']
    headers = {'Authorization': token}
    url = input('Please enter the link: ')
    bitly_url_template = 'https://api-ssl.bitly.com/v4/'
    if is_bitlink(url):
        if catch_exceptions(url, count_clicks):
            print('You entered wrong url, please try again')
            exit()
        print('Total clicks: ', count_clicks(url))
        exit()
    if catch_exceptions(url, shorten_link):
        print('You entered wrong url, please try again')
        exit()
    print('Bitlink: ', shorten_link(url))

from typing import Tuple

import requests
from bs4 import BeautifulSoup

URL = ''
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "sklep.sizeer.com",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
}


def is_available(content: str) -> bool:
    bs = BeautifulSoup(content, 'html.parser')
    markups = bs.find_all(class_='product-information')
    if len(markups) > 0:
        if markups[0].string == 'Dostępny':
            return True
    return False


def scrap_shoe_sizes(content: str) -> list:
    bs = BeautifulSoup(content, 'html.parser')
    markups = bs.find_all(class_='m-productDescr_sizeBtn js-sizeItem js-tooltipHtml js-tooltip_rm')
    return [m.string.strip() for m in markups]


def get_html(url: str, headers) -> Tuple[bool, str]:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True, response.text
    else:
        return False, 'No valid content'


if __name__ == '__main__':
    downloaded, content = get_html(URL, HEADERS)
    if downloaded:
        if is_available(content):
            sizes = scrap_shoe_sizes(content)
            print('Produkt dostepny.')
            print(sizes)
        else:
            print('Produkt niedostępny.')
    else:
        print('Nie udało się pobrać zawartości.')

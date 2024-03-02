from bs4 import BeautifulSoup
import requests


from utils.constants import ClassSelector, URLS_LIST


def get_games_list(url: str, amount: int) -> list:
    """
    Recive url, parse data, return list
    amount - limit of items in returning games_list
    """

    # get html page
    html_page = requests.get(url)

    # parse page
    soup = BeautifulSoup(html_page.text, features="html.parser")

    # find all goods cards <div>
    divs = soup.find_all('div', {"class": ClassSelector.DIV_LIST.value})

    games_list = []

    # find and extract required data
    for item_card in divs:
        img = item_card.find('img', {"class": ClassSelector.IMAGE.value})
        info, title = item_card.find_all(
            'p', {"class": ClassSelector.TITLE.value})
        price = item_card.find('p', {"class": ClassSelector.PRICE.value})

        games_list.append({
            "title": title.get_text().strip(),
            "info": info.get_text(),
            "price": price.get_text().strip(),
            "imgURL": img.attrs["src"]
        })

        # set limit items in list via amount
        if len(games_list) == amount:
            break

    return games_list


def validate_params(catalog: str, amount: str) -> bool:
    """
    validate user input data, catalog in allowed list (URLS_LIST)
    amount is digit and > 0
    """

    errors = []

    if catalog not in URLS_LIST:
        errors.append("Catalog param is not valid")

    if not amount.isdigit() or int(amount) <= 0:
        errors.append("Amount param is not valid")

    return errors

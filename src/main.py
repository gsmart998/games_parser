from bs4 import BeautifulSoup
from enum import Enum
from flask import Flask, jsonify, make_response, request
import requests


class ClassSelector(Enum):
    DIV_LIST = "my-2 ProductList-module__customCol___P96u0 col-xl-3 col-lg-3 col-md-6 col-6"
    TITLE = "ProductCard-module__cardCustomTitle___d9+Do"
    IMAGE = "card-img-top lazyImage-module__customImage___2k4hb"
    PRICE = "ProductCard-module__cardCustomPrice___No10b"


STATIC_URL = "https://ddostup.ru/catalog/"
URLS_LIST = [
    "ps-plus",
    "ps-game",
    "ps-game-addons",
    "xbox-game",
    "xbox-game-addons"
]


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


app = Flask(__name__)


@app.route('/')
def get_list():

    catalog_name = request.args.get('catalog_name')
    amount = request.args.get('amount')

    # make error respose if input data is incorrect
    errors = validate_params(catalog_name, amount)
    if len(errors) > 0:
        response = {"status": "error", "errors": errors}
        return make_response(jsonify(response), 403)

    # make url for request
    url = STATIC_URL + catalog_name

    try:
        games_list = get_games_list(url, int(amount))

    except:
        response = {"status": "error", "errors": ["Internal server error"]}
        return make_response(jsonify(response), 500)

    response = {"status": "success", "data": games_list}
    return jsonify(response)


# main function
if __name__ == '__main__':
    app.run()

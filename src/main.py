from flask import Flask, jsonify, make_response, request

from utils.constants import STATIC_URL
from utils.utils import get_games_list, validate_params


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

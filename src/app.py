import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from src.book_dao import book_dao

app = Flask(__name__)


def validate_book_payload(data):
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    title = data.get("title")
    author = data.get("author")
    price = data.get("price")

    if not isinstance(title, str) or not title.strip():
        return False, "title is required and must be a non-empty string"

    if not isinstance(author, str) or not author.strip():
        return False, "author is required and must be a non-empty string"

    try:
        price_value = float(price)
    except (TypeError, ValueError):
        return False, "price is required and must be numeric"

    if price_value < 0:
        return False, "price must be greater than or equal to 0"

    clean_data = {
        "title": title.strip(),
        "author": author.strip(),
        "price": round(price_value, 2),
    }
    return True, clean_data


def success(data, status_code=200):
    return jsonify({"status": "success", "data": data}), status_code


def error(message, status_code):
    return jsonify({"status": "error", "message": message}), status_code


@app.route('/books', methods=['GET'])
def get_all_books():
    return success(book_dao.get_all())


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = book_dao.find_by_id(id)
    if book is None:
        return error('Not found', 404)
    return success(book)


@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json(silent=True)
    is_valid, result = validate_book_payload(data)

    if not is_valid:
        return error(result, 400)

    new_id = book_dao.create(result)
    return success({'id': new_id}, 201)


@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json(silent=True)
    is_valid, result = validate_book_payload(data)

    if not is_valid:
        return error(result, 400)

    rows = book_dao.update(id, result)
    if rows == 0:
        return error('Not found', 404)
    return success({'updated': id})


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    rows = book_dao.delete(id)
    if rows == 0:
        return error('Not found', 404)
    return success({'deleted': id})


if __name__ == "__main__":
    app.run(debug=True)
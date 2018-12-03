
from flask import Flask, jsonify, request, Response
import json
from setting import *
from bookModel import *
import jwt, datetime
from userModel import User
from functools import wraps

DEFAULT_PAGE_LIMIT = 3
app.config['SECRET_KEY'] = 'mew'

@app.route('/login', methods =['POST'])
def get_token():
    request_data = request.get_json()
    if request_data:
        username = str(request_data['username'])
        password = str(request_data['password'])
        match = User.username_password_match(username, password)
        if match:
            expiration_date = str(datetime.datetime.utcnow() + datetime.timedelta(seconds=100))
            token = jwt.encode({'expiration_date':expiration_date,},app.config['SECRET_KEY'], algorithm = 'HS256')
            return token

    return Response('', status = 401, mimetype = 'application/json')

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({"error":'Need a valid token to view this page' }),401
    return wrapper

@app.route('/books')
@token_required
def getBooks():
    return jsonify({'books':Book.get_all_books()})

@app.route('/books/<int:isbn>')
def getBookByIsbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(Book.json(return_value))

def validateBook(bookObj):
    if 'name' in bookObj and 'price' in bookObj and 'isbn' in bookObj:
        return True
    return False

def validPUTrequestData(bookObj):
    if 'name' in bookObj and 'price' in bookObj:
        return True
    return False

@app.route('/books', methods = ['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if validateBook(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype="application/json")
        response.headers['Location'] = '/books/'+str(request_data['isbn'])
        return response
    invalidBookError = {
        "error":'Invalid book passed in request',
        "helpString":'Data paased in similar to this { "name": "bookname","price":7.99, "isbn":12345}'
    }
    response = Response(json.dumps(invalidBookError), status = 400, mimetype = 'application/json')
    return response

@app.route('/books/<int:isbn>', methods = ['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if not validPUTrequestData(request_data):
        invalidBookError = {
            "error":'Invalid book passed in request',
            "helpString":'Data paased in similar to this { "name": "bookname","price":7.99,}'
        }
        response = Response(json.dumps(invalidBookError), status = 400, mimetype = 'application/json')
        return response
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status = 204)
    return response

@app.route('/books/<int:isbn>', methods = ['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if 'name' in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if 'price' in request_data:
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status = 204)
    response.headers['Location'] = '/books/'+str(isbn)
    return response

@app.route('/books/<int:isbn>', methods = ['DELETE'])
@token_required
def delet_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status = 204)
        return response
    invalidBookError = {
        "error":'Book with isbn {!r} not found! Unable to DELETE'.format(isbn),
    }
    response = Response(json.dumps(invalidBookError), status = 404, mimetype = 'application/json')
    return response

app.run(port = 5000)

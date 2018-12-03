
from flask import Flask, jsonify, request, Response
import json
from setting import *
app1 = Flask(__name__)


books = [{
        "name" :'A',
        "price":1 ,
        "isbn":1234
    },
    {
        "name" :'B',
        "price":2 ,
        "isbn":1235
    },
    {
        "name" :'C',
        "price":3 ,
        "isbn":1236
    },
    {
        "name" :'D',
        "price":4 ,
        "isbn":1237
    },
    {
        "name" :'E',
        "price":5 ,
        "isbn":1238
    }
    ]

@app1.route('/books')
def getBooks():
    return jsonify({'books':books})

@app1.route('/books/<int:isbn>')
def getBookByIsbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value ={
                'name' :book['name'],
                'price' :book['price'],
                'isbn' :book['isbn']
                }
    return jsonify(return_value)

def validateBook(bookObj):
    if 'name' in bookObj and 'price' in bookObj and 'isbn' in bookObj:
        return True
    return False

def validPUTrequestData(bookObj):
    if 'name' in bookObj and 'price' in bookObj:
        return True
    return False

@app1.route('/books', methods = ['POST'])
def add_book():
    request_data = request.get_json()
    if validateBook(request_data):
        new_book ={
            'name' :request_data['name'],
            'price':request_data['price'],
            'isbn' :request_data['isbn']
            }
        books.insert(0, new_book)
        response = Response("", 201, mimetype="application/json")
        response.headers['Location'] = '/books/'+str(new_book['isbn'])
        return response
    invalidBookError = {
        "error":'Invalid book passed in request',
        "helpString":'Data paased in similar to this { "name": "bookname","price":7.99, "isbn":12345}'
    }
    response = Response(json.dumps(invalidBookError), status = 400, mimetype = 'application/json')
    return response

@app1.route('/books/<int:isbn>', methods = ['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not validPUTrequestData(request_data):
        invalidBookError = {
            "error":'Invalid book passed in request',
            "helpString":'Data paased in similar to this { "name": "bookname","price":7.99,}'
        }
        response = Response(json.dumps(invalidBookError), status = 400, mimetype = 'application/json')
        return response

    new_book ={
        'name' :request_data['name'],
        'price':request_data['price'],
        'isbn' :isbn
        }
    i = 0
    for book in books:
        currentIsbn = book['isbn']
        if currentIsbn == isbn:
            books[i] = new_book
        i+=1
    response = Response("", status = 204)
    return response

@app1.route('/books/<int:isbn>', methods = ['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    update_book = {}
    if 'name' in request_data:
        update_book['name'] = request_data['name']
    if 'price' in request_data:
        update_book['price'] = request_data['price']
    for book in books:
        if book['isbn']==isbn:
            book.update(update_book)
    response = Response("", status = 204)
    response.headers['Location'] = '/books/'+str(isbn)
    return response

@app1.route('/books/<int:isbn>', methods = ['DELETE'])
def delet_book(isbn):
    i=0
    for book in books:
        if book['isbn'] == isbn:
            books.pop(i)
            response = Response("", status = 204)
            return response
        i+=1
    invalidBookError = {
        "error":'Book with isbn {!r} not found! Unable to DELETE'.format(isbn),
    }
    response = Response(json.dumps(invalidBookError), status = 404, mimetype = 'application/json')
    return response










app1.run(port = 5000)

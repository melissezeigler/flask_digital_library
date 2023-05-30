from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'lib': 'rarry'}

@api.route('/data')
def viewdata():
    data = get_book()
    response = jsonify(data)
    print(response)
    return render_template('index.html', data = data)

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    book_title = request.json['book_title']
    author_name = request.json['author_name']
    book_length = request.json['book_length']
    type_of_cover = request.json['type_of_cover']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(book_title, author_name, book_length, type_of_cover, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# GET ALL books
@api.route('/books', methods = ['GET'])
@token_required
def get_all_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# GET SINGLE book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)
   

# UPDATE book
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.book_title = request.json['book_title']
    book.author_name = request.json['author_name']
    book.book_length = request.json['book_length']
    book.type_of_cover = request.json['type_of_cover']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE book 
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)






import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger import swagger
from sqlalchemy.orm import backref






app = Flask(__name__)
swagger = swagger(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://flask:password@localhost:5432/flask_sample"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    def __repr__(self):
        return f"<Product {self.name}>"
    
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    def __repr__(self):
        return f"<Product {self.name}>"
    
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", backref=backref("users", uselist=False))

    def __repr__(self):
        return f"<Product {self.name}>"

    
@app.route("/")
def index():
    return jsonify([{"success":"ok"}])


@app.route("/products")
def list_products():
    # Query all products from the database
    products = Product.query.paginate(page=1, per_page=1, error_out=False)
    
    # Serialize the product data
    sock_text = '<ul>'
    for sock in products:
        sock_text += '<li>' + sock.name + '</li>'
    sock_text += '</ul>'
    return sock_text
    
    # Return the serialized product data as JSON
    # return jsonify(serialized_products)


@app.route("/books")
def list_books_with_user():
    # Query books with associated user data
    books_with_user = db.session.query(Book, User).join(User).all()

    # Serialize the data
    books_data = []
    for book, user in books_with_user:
        book_data = {
            "id": book.id,
            "name": book.name,
            "user": {
                "id": user.id,
                "name": user.name
            }
        }
        books_data.append(book_data)

    # Return the data in the response
    return jsonify(books_data)
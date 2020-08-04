from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

print()
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")

class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author

    id = ma.auto_field()
    name = ma.auto_field()
    books = ma.auto_field()


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True


db.create_all()
author_schema = AuthorSchema()
book_schema = BookSchema()
author = Author(name="Chuck Paluhniuk")
book = Book(title="Fight Club", author=author)
book1 = Book(title="street fighter", author=author)
db.session.add(author)
db.session.add(book)
db.session.commit()
print(author_schema.dump(author))
# {'id': 1, 'name': 'Chuck Paluhniuk', 'books': [1]}
print( author_schema.dump(book) )



# class BookSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Book
#
#     author = ma.HyperlinkRelated("author_detail")

# with app.test_request_context():
#     print(author_schema.dump(author))
# # {'id': 1, 'name': 'Chuck Paluhniuk', 'books': ['/books/1']}
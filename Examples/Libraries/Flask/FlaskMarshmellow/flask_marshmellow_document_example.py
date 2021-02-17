from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

# Order matters: Initialize SQLAlchemy before Marshmallow
reddit_db = SQLAlchemy(app)
ma = Marshmallow(app)


class Author(reddit_db.Model):
    id = reddit_db.Column(reddit_db.Integer, primary_key=True)
    name = reddit_db.Column(reddit_db.String(255))


class Book(reddit_db.Model):
    id = reddit_db.Column(reddit_db.Integer, primary_key=True)
    title = reddit_db.Column(reddit_db.String(255))
    author_id = reddit_db.Column(
        reddit_db.Integer, reddit_db.ForeignKey("author.id")
    )
    author = reddit_db.relationship("Author", backref="books")


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


reddit_db.create_all()

author_schema = AuthorSchema()
book_schema = BookSchema()

author = Author(name="Chuck Paluhniuk")
book = Book(title="Fight Club", author=author)
book1 = Book(title="street fighter", author=author)

# # what are the other way to do this ?
# db.session.add(author)
# db.session.add(book)
# db.session.commit()
# print(author_schema.dump(author))
# print( author_schema.dump(book) )

# this have to be request context? in what scerio that it would consider as request context?

with app.test_request_context():  # session, q

    print(author_schema.dump(author))
    print(author_schema.dump(book))

# view
@app.route("/api/book/")
def users():
    all_book = Book.all()
    return book_schema.dump(all_book)


@app.route("/api/book/<id>")
def user_detail(id):
    book = Book.get(id)
    return book_schema.dump(book)


@app.route("/api/")
def user_api():
    return "it is connected"
    # return user_schema.dump(user)


# with app.test_request_context():

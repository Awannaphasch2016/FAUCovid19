from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
reddit_db = SQLAlchemy(app)


class User(reddit_db.Model):
    id = reddit_db.Column(reddit_db.Integer, primary_key=True)
    username = reddit_db.Column(
        reddit_db.String(80), unique=True, nullable=False
    )
    email = reddit_db.Column(
        reddit_db.String(120), unique=True, nullable=False
    )

    def __repr__(self):
        return "<User %r>" % self.username


if __name__ == "__main__":
    reddit_db.create_all()
    admin = User(username="admin", email="admin@example.com")
    guest = User(username="guest", email="guest@example.com")

    # # add to database
    # db.session.add(admin)
    # db.session.add(guest) #
    # db.session.commit()

    # print(User.query.all())
    print(User.query.all())
    print("-------")
    print(User.query.filter_by(username="admin").first())
    print("-------")

"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
        """"cupcakes"""

        __tablename__ = "cupcake"

        id = db.Column(
                db.Integer,
                primary_key=True,
                autoincrement=True,
        )

        flavor = db.Column(
                db.String(50),
                nullable=False,
        )

        size = db.Column(
                db.String(10),
                nullable=True,
        )

        rating = db.Column(
                db.Float,
        )

        image = db.Column(
                db.Text,
                default="https://tinyurl.com/demo-cupcake",
        )

# Each piece inside of db.Column(A, B, C, D) is called a constructor argument. So "Column" in SqlAlchemy is called a constructor. 
# Constructor=a special method that is used to initialize an object when it is created.
# Sooo.... 
# 
# db.Column(db.String(10), nullable=True, primary_key=True,)
# db.Column=Constructor
# db.String(10)=constructor argument
# nullable  = constructor Argument
# primary_key= constructor Argument
# 


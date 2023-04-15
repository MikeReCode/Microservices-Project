from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
import os
import json


app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{str(os.getenv("MYSQL_USER"))}:{str(os.getenv("MYSQL_PASSWORD"))}@{str(os.getenv("MYSQL_HOST"))}/{str(os.getenv("MYSQL_DB"))}'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:secret@db/maindm"
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ^ to migrate the database use the following commands from:  https://flask-migrate.readthedocs.io/en/latest/
# flask --app main_flask db init
# flask --app main_flask db migrate
# flask --app main_flask db upgrade


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/')
def index():
    return f'mysql://{str(os.getenv("MYSQL_USER"))}:{str(os.getenv("MYSQL_PASSWORD"))}@{str(os.getenv("MYSQL_HOST"))}/{str(os.getenv("MYSQL_DB"))}'

@app.route('/todo/')
def todo():
    product = Product.query.all()
    print(product)
    print(len(product))
    return "hello"


if __name__ == "__main__":
    
    app.run(debug=True, host='0.0.0.0')
from flask import Flask, jsonify, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
import os
import json
from dataclasses import dataclass
import requests
from producer import publish

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

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    __table_args__ =(UniqueConstraint('user_id', 'product_id', name='user_product_unique'),)

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=["POST"])
def like(id):
    req = requests.get("http://docker.for.mac.localhost:8000/api/user")
    json_req = req.json()

    try:
        productUser = ProductUser(user_id=json_req["id"], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish("product_liked", id)

    except:
        abort(400, "You already liked this product")
    return jsonify({"message": "success"})


if __name__ == "__main__":
    
    app.run(debug=True, host='0.0.0.0')
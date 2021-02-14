from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pareshtoon'
app.config['MYSQL_PASSWORD'] = 'ITACHI@21'
app.config['MYSQL_DB'] = 'pareshtoon'
mysql = MySQL(app)




@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from tags")
    if resultValue > 0:
        userDetails = cur.fetchall()
        assert isinstance(userDetails, object)
        print(userDetails)
        response = jsonify(userDetails)
        return response
        #return render_template('users.html',userDetails=userDetails)


#CORS(app)
#
# db = SQLAlchemy(app)
#
#
# @dataclass
# class Product(db.Model):
#     id: int
#     title: str
#     image: str
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=False)
#     title = db.Column(db.String(200))
#     image = db.Column(db.String(200))
#
#
# @dataclass
# class ProductUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     product_id = db.Column(db.Integer)
#
#     UniqueConstraint('user_id', 'product_id', name='user_product_unique')
#
#
# @app.route('/api/products')
# def index():
#     return jsonify(Product.query.all())
#
#
# @app.route('/api/products/<int:id>/like', methods=['POST'])
# def like(id):
#     req = requests.get('http://docker.for.mac.localhost:8000/api/user')
#     json = req.json()
#
#     try:
#         productUser = ProductUser(user_id=json['id'], product_id=id)
#         db.session.add(productUser)
#         db.session.commit()
#
#         publish('product_liked', id)
#     except:
#         abort(400, 'You already liked this product')
#
#     return jsonify({
#         'message': 'success'
#     })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

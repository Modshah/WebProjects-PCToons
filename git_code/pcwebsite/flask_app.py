from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

db = SQLAlchemy(app)
@app.route('/')
def index():
    return 'Hello'

if __name__=='__main__':
    app.run(host='0.0.0.0')
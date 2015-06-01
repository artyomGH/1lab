from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restless import *
import os

app = Flask(__name__)
#app.config.update(SERVER_NAME='localhost:5010')
DB_PATH = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/register.db'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH  # 'sqlite:////tmp/register.db'
db = SQLAlchemy(app)

borjnuku = db.Table('borjnuku',
                   db.Column('obtaj_id', db.Integer, db.ForeignKey('obtaj.id')),
                   db.Column('borj_id', db.Integer, db.ForeignKey('borjnuk.id'))
                   )

class Borjnuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    tel_number = db.Column(db.Integer())

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_property = db.Column(db.String(200), unique=True)
    ser_number = db.Column(db.String(200), unique=True)
    obtaj_id=db.Column(db.Integer,db.ForeignKey('obtaj.id'))

class Obtaj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason_doc = db.Column(db.String(200), unique=True)
    cost_size=db.Column(db.Integer)
    borjnuku = db.relationship('Borjnuk', secondary=borjnuku,
                              backref=db.backref('obtajennas', lazy='dynamic')
                              )
    properties = db.relationship('Property',
                              backref='majno',
                              lazy='dynamic')

@app.route('/')
def index():
    return render_template('Index.html')


if __name__ == '__main__':

    mr_manager = APIManager(app, flask_sqlalchemy_db=db)
    mr_manager.create_api(Obtaj, methods=['GET', 'POST'])# , exclude_columns=['methods'])
    mr_manager.create_api(Borjnuk, methods=['GET', 'POST'])# , include_columns=['id', 'name', 'methods', 'methods.name'])
    mr_manager.create_api(Property, methods=['GET', 'POST', 'PATCH', 'DELETE'])#,
                          # include_columns=['id', 'name', 'authors', 'authors.name', 'category', 'category.name',
                          #                  'creation_date', 'approval_date'])
    app.run(host='127.0.0.1', port=5010)
    # print(DB_PATH)
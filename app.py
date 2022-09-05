"""
Multiagent Project Companion

API Made to store data for the simulations in
multiAgents Projects.

NOT AS SECURE AS IT SHOULD BE :P
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date


app = Flask(__name__)

# Config Settings
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///multiagents.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# DB CONFIG
db = SQLAlchemy(app=app)

migrate = Migrate(app, db)


# Models
class Simulacion(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    rel_date = db.Column('Date', db.Date, default=date.today())
    cant_carros = db.Column('Cantidad Carros', db.Integer)
    colisiones = db.Column('Colisiones', db.Integer)
    tiempo_total = db.Column('Tiempo Total', db.Integer)


    def __init__(self, rel_date, cant_carros, colisiones, t_time):
        self.rel_date = rel_date
        self.cant_carros = cant_carros
        self.colisiones = colisiones
        self.tiempo_total = t_time


    def to_dict(self):
        return {
            'id':self._id,
            'rel_date':self.rel_date,
            'cant_carros': self.cant_carros,
            'colisiones': self.colisiones,
            'tiempo_total': self.tiempo_total
        }



@app.route('/')
def home():
    return {'hello':'hello'}



@app.route('/sims', methods=['GET', 'POST'])
def sims():
    
    if request.method == 'POST':
        data = request.json

        try: 
            sim = Simulacion(date.today(), data['cant_carros'], data['colisiones'], data['t_time'])
            db.session.add(sim)
            db.session.commit()
        except:
            db.session.rollback()
            return 'Algo salio mal', 400

        return data

    if request.method == 'GET':
        sims = Simulacion.query.all()
        
        sims = [item.to_dict() for item in sims]
        return {'sims': sims}, 200

    return 'hello'


@app.route('/sim/<id>', methods=['GET', 'PUT', 'DELETE'])
def sim(id):

    try:
        sim = Simulacion.query.get(id)
    except:
        return 'Not Found', 404


    if request.method == 'GET':
        return {'sim': sim.to_dict()}, 200


    if request.method == 'DELETE':
        try:
            db.session.delete(sim)
            db.session.commit()
        except:
            db.session.rollback()
        
        return {"sim", sim}, 200
        


    if request.method == 'PUT':

        data = request.json

        try:
            sim.rel_date = data['rel_date'] if 'rel_date' in data.keys() else sim.rel_date
            sim.cant_carros = data['cant_carros'] if 'cant_carros' in data.keys() else sim.cant_carros
            sim.colisiones = data['colisiones'] if 'colisiones' in data.keys() else sim.colisiones
            sim.tiempo_total = data['t_time'] if 't_time' in data.keys() else sim.tiempo_total
            db.session.commit()
        except:
            return 'OOps, Algo salio mal!', 400

        return sim.to_dict()


    return 'method not allowed', 405

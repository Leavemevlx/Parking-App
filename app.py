from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
db = SQLAlchemy(app)

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(200), nullable =False)
    status = db.Column(db.Boolean, default=True)
    total_spots = db.Column(db.Integer, nullable=False)
    spots_taken = db.Column(db.Integer, nullable=False)

class SpotEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id= db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False)

@app.route('/')

def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

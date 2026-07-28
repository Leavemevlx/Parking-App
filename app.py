from flask import Flask, render_template, url_for,redirect
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
    #fetch the lots here
    lots = quick_sort(ParkingLot.query.all())
    return render_template('index.html', lots=lots)

# make the take_spot
@app.route('/take_spot/<lot_id>', methods=['POST'])

def take_spot(lot_id):
    # get the lots by it's id
    spot = ParkingLot.query.get(lot_id)
    # when the spot is taken, add 1 to spots_taken
    spot.spots_taken += 1
    # save it to the database
    db.session.commit()
    # return it to the homepage
    return redirect(url_for('index'))

# make the spot become open
@app.route('/free_spot/<lot_id>', methods=['POST'])

def free_spot(lot_id):
    # get the lot from the id
    spot = ParkingLot.query.get(lot_id)
    # when it becomes open, make it 0
    if spot.spots_taken != 0:
    
        spot.spots_taken -= 1
        # save it to the database
        db.session.commit()
        # return it to the homepage
        return redirect(url_for('index'))
    return redirect(url_for('index'))

def quick_sort(lots):
    if len(lots) <= 1:
        return lots
    
    pivot = lots[len(lots) // 2]
    left = [lot for lot in lots if lot.spots_taken <= pivot.spots_taken if lot != pivot]
    right = [lot for lot in lots if lot.spots_taken > pivot.spots_taken if lot != pivot]
    
    return quick_sort(left) + [pivot] + quick_sort(right)

if __name__ == "__main__":
    app.run(debug=True)

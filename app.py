from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # Simple SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    host = db.Column(db.String(50))
    template = db.Column(db.String(20), default="modern")
    rsvpDeadline = db.Column(db.String(20))

db.create_all()

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(
        title=data.get('title'),
        date=data.get('date'),
        time=data.get('time'),
        location=data.get('location'),
        description=data.get('description'),
        host=data.get('host'),
        template=data.get('template'),
        rsvpDeadline=data.get('rsvpDeadline')
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'id': new_event.id})

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'date': e.date,
        'time': e.time,
        'location': e.location,
        'description': e.description,
        'host': e.host,
        'template': e.template,
        'rsvpDeadline': e.rsvpDeadline
    } for e in events])

if __name__ == '__main__':
    app.run(debug=True)

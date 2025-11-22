from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models after db is initialized
from models import Event

# Routes
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
    return jsonify({'id': new_event.id}), 201

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
    } for e in events]), 200

if __name__ == '__main__':
    # Only create tables when running directly
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///connect.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS - Allow frontend to connect
CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)

# ========== MODELS ==========
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    host = db.Column(db.String(100))
    template = db.Column(db.String(50), default='modern')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    group = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')

# ========== ROUTES ==========

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Backend is running!'}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        full_name=data.get('full_name', '')
    )
    db.session.add(user)
    db.session.commit()
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name
        }
    }), 200

@app.route('/api/events', methods=['GET'])
def get_events():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        events = Event.query.filter_by(user_id=payload['user_id']).all()
        return jsonify([{
            'id': e.id,
            'title': e.title,
            'date': e.date,
            'time': e.time,
            'location': e.location,
            'description': e.description,
            'host': e.host,
            'template': e.template
        } for e in events]), 200
    except:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/events', methods=['POST'])
def create_event():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        data = request.get_json()
        
        event = Event(
            user_id=payload['user_id'],
            title=data['title'],
            date=data.get('date'),
            time=data.get('time'),
            location=data.get('location'),
            description=data.get('description'),
            host=data.get('host'),
            template=data.get('template', 'modern')
        )
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'id': event.id,
            'message': 'Event created successfully'
        }), 201
    except:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        contacts = Contact.query.filter_by(user_id=payload['user_id']).all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'phone': c.phone,
            'email': c.email,
            'group': c.group,
            'status': c.status
        } for c in contacts]), 200
    except:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/contacts', methods=['POST'])
def create_contact():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        data = request.get_json()
        
        contact = Contact(
            user_id=payload['user_id'],
            name=data['name'],
            phone=data.get('phone'),
            email=data.get('email'),
            group=data.get('group'),
            status='pending'
        )
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({'id': contact.id, 'message': 'Contact created'}), 201
    except:
        return jsonify({'error': 'Invalid token'}), 401
        
@app.route('/')
def home():
    return "Connect Celebrate Backend is running!"

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

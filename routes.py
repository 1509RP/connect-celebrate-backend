from flask import Blueprint, request, jsonify
from models import Event, Contact, Voice, Manage
from extensions import db

bp = Blueprint('api', __name__)

# Event routes
@bp.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(**data)
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'id': new_event.id}), 201

@bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([e.__dict__ for e in events])

# Contact routes
@bp.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    new_contact = Contact(**data)
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'id': new_contact.id}), 201

@bp.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([c.__dict__ for c in contacts])

# Voice routes
@bp.route('/voice', methods=['POST'])
def create_voice():
    data = request.get_json()
    new_voice = Voice(**data)
    db.session.add(new_voice)
    db.session.commit()
    return jsonify({'id': new_voice.id}), 201

@bp.route('/voice', methods=['GET'])
def get_voice():
    voices = Voice.query.all()
    return jsonify([v.__dict__ for v in voices])

# Manage routes
@bp.route('/manage', methods=['POST'])
def create_manage():
    data = request.get_json()
    new_manage = Manage(**data)
    db.session.add(new_manage)
    db.session.commit()
    return jsonify({'id': new_manage.id}), 201

@bp.route('/manage', methods=['GET'])
def get_manage():
    tasks = Manage.query.all()
    return jsonify([t.__dict__ for t in tasks])

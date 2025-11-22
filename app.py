from flask import Flask, request, jsonify
from extensions import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    from models import Event, Contact, Voice, Manage

    # ----- Event Routes -----
    @app.route('/api/events', methods=['POST'])
    def create_event():
        data = request.get_json()
        e = Event(**data)
        db.session.add(e)
        db.session.commit()
        return jsonify({'id': e.id}), 201

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

    # ----- Contact Routes -----
    @app.route('/api/contacts', methods=['POST'])
    def create_contact():
        data = request.get_json()
        c = Contact(**data)
        db.session.add(c)
        db.session.commit()
        return jsonify({'id': c.id}), 201

    @app.route('/api/contacts', methods=['GET'])
    def get_contacts():
        contacts = Contact.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'email': c.email,
            'message': c.message
        } for c in contacts])

    # ----- Voice Routes -----
    @app.route('/api/voice', methods=['POST'])
    def add_voice():
        data = request.get_json()
        v = Voice(**data)
        db.session.add(v)
        db.session.commit()
        return jsonify({'id': v.id}), 201

    @app.route('/api/voice', methods=['GET'])
    def get_voice():
        voices = Voice.query.all()
        return jsonify([{
            'id': v.id,
            'command': v.command,
            'response': v.response
        } for v in voices])

    # ----- Manage Routes -----
    @app.route('/api/manage', methods=['POST'])
    def add_task():
        data = request.get_json()
        m = Manage(**data)
        db.session.add(m)
        db.session.commit()
        return jsonify({'id': m.id}), 201

    @app.route('/api/manage', methods=['GET'])
    def get_tasks():
        tasks = Manage.query.all()
        return jsonify([{
            'id': t.id,
            'task': t.task,
            'status': t.status
        } for t in tasks])

    @app.route('/api/manage/<int:id>', methods=['PUT'])
    def update_task(id):
        t = Manage.query.get_or_404(id)
        data = request.get_json()
        t.task = data.get('task', t.task)
        t.status = data.get('status', t.status)
        db.session.commit()
        return jsonify({'msg': 'updated'})

    @app.route('/api/manage/<int:id>', methods=['DELETE'])
    def delete_task(id):
        t = Manage.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return jsonify({'msg': 'deleted'})

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)

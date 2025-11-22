from app import db

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

from app import app, db

def create_db():
    """Create all tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created!")

def drop_db():
    """Drop all tables"""
    with app.app_context():
        db.drop_all()
        print("Database tables dropped!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python manage.py [create|drop]")
    elif sys.argv[1] == "create":
        create_db()
    elif sys.argv[1] == "drop":
        drop_db()
    else:
        print("Unknown command")

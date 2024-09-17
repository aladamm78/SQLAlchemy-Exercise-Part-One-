from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, default='https://via.placeholder.com/150')

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

def connect_db(app):
    """Connect the database to the provided Flask app."""
    db.app = app
    db.init_app(app)


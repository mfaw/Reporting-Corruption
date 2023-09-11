from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    reports = db.relationship('Report', backref='user', lazy=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=True)
    mobile = db.Column(db.String(15), nullable=True)
    points = db.Column(db.Integer, default=0, nullable=False)
    ip_address = db.Column(db.String(80), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)

    # Add the following Flask-Login required attributes
    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        # You can implement custom logic for user activation here if needed
        return True

    @property
    def is_authenticated(self):
        return True  # Assuming all users are authenticated

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return f'<User {self.username}>'


class ReportCategoryEnum(Enum):
    GENERAL = 'General'
    SAFETY = 'Safety'
    ENVIRONMENT = 'Environment'


class Report(db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True)
    report_text = db.Column(db.Text, nullable=False)
    category = db.Column(ENUM(ReportCategoryEnum), nullable=True)  # PostgreSQL ENUM
    location_lat = db.Column(db.Float, nullable=True)
    location_lang = db.Column(db.Float, nullable=True)
    location_name = db.Column(db.String(255), nullable=True)
    authenticity_before = db.Column(db.Float, nullable=True)
    authenticity_after = db.Column(db.Float, nullable=True)
    points_given = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

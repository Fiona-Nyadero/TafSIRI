from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy.types import Float

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    Email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    Password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    Phone_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    Date_of_birth: so.Mapped[Optional[date]] = so.mapped_column(sa.Date)
    About_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    Last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    Type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10))
    Job_title: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))

    Projects: so.WriteOnlyMapped['Project'] = so.relationship(
        back_populates='Author')
    
    Response: so.WriteOnlyMapped['Feedback'] = so.relationship(
        back_populates='Responsee')

    def __repr__(self):
        return '<User {}>'.format(self.Username)
    
    def set_password(self, password):
        self.Password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.Email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Title: so.Mapped[str] = so.mapped_column(sa.String(256))
    Timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    #Project page deets
    User_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    Cover: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10)) #Yes or No
    Description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    Background: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1024))
    Proposal: so.Mapped[Optional[str]] = so.mapped_column(sa.String(2048))
    Phase: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))
            # Phase examples: Conception, Tendering, Construction, Operation(DLP), Stalled
    # Extent: plot boundaries on a map
        # Photos: link to 3d renders
    Photo1_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120)) #To be
    Photo2_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120)) #used
    Photo3_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10)) #later
        # Documents: plans and specifications
    Plan: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120)) #Yes or No
    Deadline: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime)
        # Feedback_period: when project is open for feedback
    SDGs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))

    #Catalogue page deets
    County: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    Latitude: so.Mapped[Optional[float]] = so.mapped_column(sa.Float(20))
    Longitude: so.Mapped[Optional[float]] = so.mapped_column(sa.Float(20))
    Category: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    Author: so.Mapped[User] = so.relationship(back_populates='Projects')
    Feedback_received: so.Mapped['Feedback'] = so.relationship(back_populates='Feedback_project')
    

    def __repr__(self):
        return '<Project {}>'.format(self.Title)

class Feedback(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Rating: so.Mapped[int] = so.mapped_column(sa.Integer)
    Rating_reason: so.Mapped[str] = so.mapped_column(sa.String(1024))
    Suggestions: so.Mapped[str] = so.mapped_column(sa.String(1024))
    Submitted: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    Responsee_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    
    Responsee: so.Mapped[User] = so.relationship(back_populates='Response')

    Feedback_project_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Project.id),
                                               index=True)
    Feedback_project: so.Mapped[Project] = so.relationship(back_populates='Feedback_received')

    def __repr__(self):
        return f'<Feedback id={self.id} rating={self.Rating} responsee={self.Responsee_id} feedback_project={self.Feedback_project_id}>'
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
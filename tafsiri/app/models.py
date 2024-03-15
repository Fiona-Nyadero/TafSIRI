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

    Projects: so.WriteOnlyMapped['Project'] = so.relationship(
        back_populates='Author')

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
    # Cover_photo: Hero section/Catalogue thumbnail
    Description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    Background: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1024))
    Proposal: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1024))
    Phase: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))
            # Phase examples: Conception, Tendering, Construction, Operation(DLP), Stalled
    # Extent: plot boundaries on a map
    # Photos: link to 3d renders
    # Feedback_id: foreign key(dont know how yet)
    # Feedback_period: when project is open for feedback
    # SDG_id: foreign key
    # Contact_person: Author(user-id)

    #Catalogue page deets
    # Cover_photo: Hero section/Catalogue thumbnail
    # Location_id: County(can be a foreign key)
    Latitude: so.Mapped[Optional[float]] = so.mapped_column(Float(20))
    Longitude: so.Mapped[Optional[float]] = so.mapped_column(Float(20))
    # Category_id: project type(can be a foreign key)
    Author: so.Mapped[User] = so.relationship(back_populates='Projects')
    

    def __repr__(self):
        return '<Project {}>'.format(self.Title)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
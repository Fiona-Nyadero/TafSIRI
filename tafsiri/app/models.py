from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    Email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    Password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    Phone_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    Date_of_birth: so.Mapped[Optional[date]] = so.mapped_column(sa.Date)

    Projects: so.WriteOnlyMapped['Project'] = so.relationship(
        back_populates='Author')

    def __repr__(self):
        return '<User {}>'.format(self.Username)
    
    def set_password(self, password):
        self.Password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password_hash, password)
    
class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Title: so.Mapped[str] = so.mapped_column(sa.String(256))
    Timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    User_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    Author: so.Mapped[User] = so.relationship(back_populates='Projects')
    # Description:Location:Category:Status:cd 

    def __repr__(self):
        return '<Project {}>'.format(self.Title)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
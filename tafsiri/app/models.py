from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    Email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    Password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    Projects: so.WriteOnlyMapped['Project'] = so.relationship(
        back_populates='Author')

    def __repr__(self):
        return '<User {}>'.format(self.Username)
    
class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Title: so.Mapped[str] = so.mapped_column(sa.String(256))
    Timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    User_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    Author: so.Mapped[User] = so.relationship(back_populates='Projects')
    # Description:Location:Category:Status:

    def __repr__(self):
        return '<Project {}>'.format(self.Title)
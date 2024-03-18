from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy.types import Float
from app.models import User, followers

class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Title: so.Mapped[str] = so.mapped_column(sa.String(256))
    Timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    #Project page deets
    User_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    # Cover_image: Hero section/Catalogue thumbnail
    Description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    Background: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1024))
    Proposal: so.Mapped[Optional[str]] = so.mapped_column(sa.String(1024))
    Phase: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))
            # Phase examples: Conception, Tendering, Construction, Operation(DLP), Stalled
    # Extent: plot boundaries on a map
    # Images: link to 3d renders
    # Documents: link to plans and specifications
    # Project_feedback: (linked to particular user)(linked to particular feedback)
    Deadline: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime)
        # Feedback_period: when project is open for feedback
    SDGs: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))

    #Catalogue page deets
    # Cover_image: Hero section/Catalogue thumbnail(see above)
    Location: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    Latitude: so.Mapped[Optional[float]] = so.mapped_column(sa.Float(20))
    Longitude: so.Mapped[Optional[float]] = so.mapped_column(sa.Float(20))
    Category: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    Author: so.Mapped[User] = so.relationship(back_populates='Projects')
        # Contact_person: Author(user-id)
    Followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == User.id),
        back_populates='Projects_following',
        lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.Title)
    
    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.Followers.select().subquery())
        return db.session.scalar(query)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, SelectField, DateTimeField, FloatField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User, Project

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('Phone Number') 
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    user_type = SelectField('User Type', choices=[('Regular', 'Regular'), ('Admin', 'Admin')], default='Regular')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.Username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.Email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    job_title = TextAreaField('Job title', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])
    phase = SelectField('Phase', choices=[('Conception', 'Conception'), ('Tendering', 'Tendering'),
                                          ('Construction', 'Construction'), ('Operation', 'Operation'),
                                          ('Operation(PostDLP)', 'Operation(PostDLP)'),
                                          ('Stalled', 'Stalled')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('About me', validators=[Length(min=0, max=256)])
    background = TextAreaField('About me', validators=[Length(min=0, max=1024)])
    proposal = TextAreaField('About me', validators=[Length(min=0, max=2048)])
    deadline = DateTimeField('Deadline', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Latitude', validators=[DataRequired()])
    phase = SelectField('Phase', choices=[('Conception', 'Conception'), ('Tendering', 'Tendering'),
                                          ('Construction', 'Construction'), ('Operation', 'Operation'),
                                          ('Operation(PostDLP)', 'Operation(PostDLP)'),
                                          ('Stalled', 'Stalled')], validators=[DataRequired()])
    category = SelectField('Category', choices=[('Community', 'Community'), ('Culture', 'Culture'),
                                                ('Education', 'Education'),
                                                ('Environment', 'Environment'), ('Health', 'Health'),
                                                ('Planning', 'Planning'), ('Recreation', 'Recreation'),
                                                ('Technology', 'Technology'), ('Transportation', 'Transportation'),
                                                ('MegaProject', 'MegaProject'), ('Undefined', 'Undefined')],
                                                validators=[DataRequired()], default='Undefined')
    sdgs = StringField('SDGs', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    rating_reason = TextAreaField('Rating_reason', validators=[Length(min=0, max=1024)])
    suggestions = TextAreaField('Suggestions', validators=[Length(min=0, max=1024)])
    submit = SubmitField('Submit')
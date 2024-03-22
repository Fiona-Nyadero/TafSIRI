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
    user_type = SelectField('User Type', choices=[('Regular', 'Regular'), ('Admin', 'Admin')], default='Regular')
    submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])
    phase = SelectField('Phase', choices=[('Conception', 'Conception'), ('Tendering', 'Tendering'),
                                          ('Construction', 'Construction'), ('Operation', 'Operation'),
                                          ('Operation(PostDLP)', 'Operation(PostDLP)'),
                                          ('Stalled', 'Stalled')], validators=[DataRequired()])
    cover = SelectField('Cover', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], default='No')
    plan = SelectField('Plan', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], default='No')
    background = TextAreaField('Background', validators=[Length(min=0, max=1024)])
    proposal = TextAreaField('Proposal', validators=[Length(min=0, max=2048)])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Community', 'Community'), ('Culture', 'Culture'),
                                                ('Education', 'Education'),
                                                ('Environment', 'Environment'), ('Health', 'Health'),
                                                ('Housing', 'Housing'),
                                                ('Planning', 'Planning'), ('Recreation', 'Recreation'),
                                                ('Technology', 'Technology'), ('Transportation', 'Transportation'),
                                                ('MegaProject', 'MegaProject'), ('Undefined', 'Undefined')],
                                                validators=[DataRequired()], default='Undefined')
    sdgs_choices = [
        ('01 No Poverty', '01 No Poverty'), ('02 Zero Hunger', '02 Zero Hunger'),
        ('03 Good Health and Well-being', '03 Good Health and Well-being'),
        ('04 Quality Education', '04 Quality Education'), ('05 Gender Equality', '05 Gender Equality'),
        ('06 Clean Water and Sanitation', '06 Clean Water and Sanitation'),
        ('07 Affordable and Clean Energy', '07 Affordable and Clean Energy'),
        ('08 Decent Work and Economic Growth', '08 Decent Work and Economic Growth'),
        ('09 Industry, Innovation and Infrastructure', '09 Industry, Innovation and Infrastructure'),
        ('10 Reduced Inequalities', '10 Reduced Inequalities'),
        ('11 Sustainable Cities and Communities', '11 Sustainable Cities and Communities'),
        ('12 Responsible Consumption and Production', '12 Responsible Consumption and Production'),
        ('13 Climate Action', '13 Climate Action'),
        ('14 Life Below Water', '14 Life Below Water'), ('15 Life on Land', '15 Life on Land'),
        ('16 Peace, Justice and Strong Institutions', '16 Peace, Justice and Strong Institutions'),
        ('17 Patnerships for the Goals', '17 Patnerships for the Goals')
    ]
    sdgs = SelectField('SDGs', choices=sdgs_choices, validators=[DataRequired()])
    county_choices = [
        ('Baringo', 'Baringo'), ('Bomet', 'Bomet'), ('Bungoma', 'Bungoma'),
        ('Busia', 'Busia'), ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
        ('Embu', 'Embu'), ('Garissa', 'Garissa'), ('Homa Bay', 'Homa Bay'),
        ('Isiolo', 'Isiolo'), ('Kajiado', 'Kajiado'), ('Kakamega', 'Kakamega'),
        ('Kericho', 'Kericho'), ('Kiambu', 'Kiambu'), ('Kilifi', 'Kilifi'),
        ('Kirinyaga', 'Kirinyaga'), ('Kisii', 'Kisii'), ('Kisumu', 'Kisumu'),
        ('Kitui', 'Kitui'), ('Kwale', 'Kwale'), ('Laikipia', 'Laikipia'),
        ('Lamu', 'Lamu'), ('Machakos', 'Machakos'), ('Makueni', 'Makueni'),
        ('Mandera', 'Mandera'), ('Marsabit', 'Marsabit'), ('Meru', 'Meru'),
        ('Migori', 'Migori'), ('Mombasa', 'Mombasa'), ('Murang\'a', 'Murang\'a'),
        ('Nairobi', 'Nairobi'), ('Nakuru', 'Nakuru'), ('Nandi', 'Nandi'),
        ('Narok', 'Narok'), ('Nyamira', 'Nyamira'), ('Nyandarua', 'Nyandarua'),
        ('Nyeri', 'Nyeri'), ('Samburu', 'Samburu'), ('Siaya', 'Siaya'),
        ('Taita-Taveta', 'Taita-Taveta'), ('Tana River', 'Tana River'),
        ('Tharaka-Nithi', 'Tharaka-Nithi'), ('Tans Nzoia', 'Trans Nzoia'),
        ('Turkana', 'Turkana'), ('Uasin Gishu', 'Uasin Gishu'),
        ('Vihiga', 'Vihiga'), ('Wajir', 'Wajir'), ('West Pokot', 'West Pokot'),
    ]
    county = SelectField('County', choices=county_choices, validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=256)])
    background = TextAreaField('Background', validators=[Length(min=0, max=1024)])
    proposal = TextAreaField('Proposal', validators=[Length(min=0, max=2048)])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    cover = SelectField('Cover', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], default='No')
    plan = SelectField('Plan', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], default='No')
    phase = SelectField('Phase', choices=[('Conception', 'Conception'), ('Tendering', 'Tendering'),
                                          ('Construction', 'Construction'), ('Operation', 'Operation'),
                                          ('Operation(PostDLP)', 'Operation(PostDLP)'),
                                          ('Stalled', 'Stalled')], validators=[DataRequired()])
    category = SelectField('Category', choices=[('Community', 'Community'), ('Culture', 'Culture'),
                                                ('Education', 'Education'),
                                                ('Environment', 'Environment'), ('Health', 'Health'),
                                                ('Housing', 'Housing'),
                                                ('Planning', 'Planning'), ('Recreation', 'Recreation'),
                                                ('Technology', 'Technology'), ('Transportation', 'Transportation'),
                                                ('MegaProject', 'MegaProject'), ('Undefined', 'Undefined')],
                                                validators=[DataRequired()], default='Undefined')
    sdgs_choices = [
        ('01 No Poverty', '01 No Poverty'), ('02 Zero Hunger', '02 Zero Hunger'),
        ('03 Good Health and Well-being', '03 Good Health and Well-being'),
        ('04 Quality Education', '04 Quality Education'), ('05 Gender Equality', '05 Gender Equality'),
        ('06 Clean Water and Sanitation', '06 Clean Water and Sanitation'),
        ('07 Affordable and Clean Energy', '07 Affordable and Clean Energy'),
        ('08 Decent Work and Economic Growth', '08 Decent Work and Economic Growth'),
        ('09 Industry, Innovation and Infrastructure', '09 Industry, Innovation and Infrastructure'),
        ('10 Reduced Inequalities', '10 Reduced Inequalities'),
        ('11 Sustainable Cities and Communities', '11 Sustainable Cities and Communities'),
        ('12 Responsible Consumption and Production', '12 Responsible Consumption and Production'),
        ('13 Climate Action', '13 Climate Action'),
        ('14 Life Below Water', '14 Life Below Water'), ('15 Life on Land', '15 Life on Land'),
        ('16 Peace, Justice and Strong Institutions', '16 Peace, Justice and Strong Institutions'),
        ('17 Patnerships for the Goals', '17 Patnerships for the Goals')
    ]
    sdgs = SelectField('SDGs', choices=sdgs_choices, validators=[DataRequired()])
    county_choices = [
        ('Baringo', 'Baringo'), ('Bomet', 'Bomet'), ('Bungoma', 'Bungoma'),
        ('Busia', 'Busia'), ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
        ('Embu', 'Embu'), ('Garissa', 'Garissa'), ('Homa Bay', 'Homa Bay'),
        ('Isiolo', 'Isiolo'), ('Kajiado', 'Kajiado'), ('Kakamega', 'Kakamega'),
        ('Kericho', 'Kericho'), ('Kiambu', 'Kiambu'), ('Kilifi', 'Kilifi'),
        ('Kirinyaga', 'Kirinyaga'), ('Kisii', 'Kisii'), ('Kisumu', 'Kisumu'),
        ('Kitui', 'Kitui'), ('Kwale', 'Kwale'), ('Laikipia', 'Laikipia'),
        ('Lamu', 'Lamu'), ('Machakos', 'Machakos'), ('Makueni', 'Makueni'),
        ('Mandera', 'Mandera'), ('Marsabit', 'Marsabit'), ('Meru', 'Meru'),
        ('Migori', 'Migori'), ('Mombasa', 'Mombasa'), ('Murang\'a', 'Murang\'a'),
        ('Nairobi', 'Nairobi'), ('Nakuru', 'Nakuru'), ('Nandi', 'Nandi'),
        ('Narok', 'Narok'), ('Nyamira', 'Nyamira'), ('Nyandarua', 'Nyandarua'),
        ('Nyeri', 'Nyeri'), ('Samburu', 'Samburu'), ('Siaya', 'Siaya'),
        ('Taita-Taveta', 'Taita-Taveta'), ('Tana River', 'Tana River'),
        ('Tharaka-Nithi', 'Tharaka-Nithi'), ('Tans Nzoia', 'Trans Nzoia'),
        ('Turkana', 'Turkana'), ('Uasin Gishu', 'Uasin Gishu'),
        ('Vihiga', 'Vihiga'), ('Wajir', 'Wajir'), ('West Pokot', 'West Pokot'),
    ]
    county = SelectField('County', choices=county_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    rating_reason = TextAreaField('Rating_reason', validators=[Length(min=0, max=1024)])
    suggestions = TextAreaField('Suggestions', validators=[Length(min=0, max=1024)])
    privacy_policy = BooleanField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
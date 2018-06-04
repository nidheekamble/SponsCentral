from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange

class SelectForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    select = RadioField('User Type',choices=[('P','sponsered Party'),('S','Sponserer')])
    submit = SubmitField('Proceed')


class RegistrationFormParty(FlaskForm):
    party_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)] )
    party_choices = ['Technical','Sports','Cultural']#add "others"
    party_type = SelectField('Type', choices=party_choices, validators=[Required()])
    party_kind = SelectField('Accepting', choices=['Cash', 'Kind'], validators=[Required()])
    party_contactNo1 = IntegerField('ContactNo1', validators=[DataRequired(), NumberRange(min=10000000, max=99999999)])
    party_contactNo2 = IntegerField('ContactNo2', validators=[DataRequired(), NumberRange(min=10000000, max=99999999)])
    party_address = TextAreaField('Address', validators=[DataRequired()])
    party_about = TextAreaField('About', validators=[DataRequired()] )
    party_fromAmount = IntegerField('From Amount', validators=[DataRequired()])
    party_toAmount = IntegerField('To Amount', validators=[DataRequired()])
    party_submit = SubmitField('Sign Up')
    party_logo = FileField('Logo')#put validators

class RegistrationFormSponser(FlaskForm):
    sponsor_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)] )
    sponsor_about = TextAreaField('About', validators=[DataRequired()] )
    sponsor_choices = ['Finance','Information Technology','Others']#add "others"
    sponsor_type = SelectField('Type Of Sponser', choices=sponsor_choices, validators=[Required()])
    sponsor_kind = SelectField('Sponser With', choices=['Cash', 'Kind'], validators=[Required()])
    sponsor_contactNo1 = StringField('ContactNo1', validators=[DataRequired(), Length(min=10, max=10)])
    sponsor_contactNo2 = StringField('ContactNo2', validators=[DataRequired(), Length(min=10, max=10)])
    sponsor_address = TextAreaField('Address', validators=[DataRequired()])
    sponsor_fromAmount = IntegerField('FromAmount', validators=[Required()])
    sponsor_toAmount = IntegerField('ToAmount', validators=[Required()])
    sponsor_submit = SubmitField('Sign Up')
    sponser_logo = FileField('Logo')#put validators


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    select = RadioField('User Type',choices=[('P','sponsered Party'),('S','Sponserer')])
    submit = SubmitField('Login')

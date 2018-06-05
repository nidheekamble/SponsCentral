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
    party_choices = [('T','Technical'),('S', 'Sports'),('C', 'Cultural')]#add "others"
    party_type = SelectField('Type', choices=party_choices, validators=[Required()])
    party_kind = SelectField('Accepting', choices=[('C','Cash'), ('k','Kind')], validators=[Required()])
    party_contactNo1 = IntegerField('ContactNo1', validators=[DataRequired(), NumberRange(min=10000000, max=99999999)])
    party_contactNo2 = IntegerField('ContactNo2', validators=[DataRequired(), NumberRange(min=10000000, max=99999999)])
    party_address = TextAreaField('Address', validators=[DataRequired()])
    party_about = TextAreaField('About Your Organization', validators=[DataRequired()] )
    party_fromAmount = IntegerField('From Amount', validators=[DataRequired()])
    party_toAmount = IntegerField('To Amount', validators=[DataRequired()])
    party_submit = SubmitField('Sign Up')
    party_logo = FileField('Logo')#put validators

class RegistrationFormSponser(FlaskForm):
    sponsor_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)] )
    sponsor_choices = [('F','Finance'),('IT','Information Technology'),('O','Others')]#add "others"
    sponsor_type = SelectField('Type Of Sponser', choices=sponsor_choices, validators=[Required()])
    sponsor_kind = SelectField('Accepting', choices=[('C','Cash'), ('k','Kind')], validators=[Required()])
    sponsor_contactNo1 = IntegerField('ContactNo1', validators=[DataRequired(), NumberRange(min=10000000, max=99999999)])
    sponsor_contactNo2 = IntegerField('ContactNo2', validators=[DataRequired(), NumberRange(min=10000000, max=99999999)])
    sponsor_address = TextAreaField('Address', validators=[DataRequired()])
    sponsor_about = TextAreaField('About Your Organization', validators=[DataRequired()])
    sponsor_fromAmount = IntegerField('From Amount', validators=[Required()])
    sponsor_toAmount = IntegerField('To Amount', validators=[Required()])
    sponsor_submit = SubmitField('Sign Up')
    sponsor_logo = FileField('Logo')#put validators


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    select = RadioField('User Type',choices=[('P','sponsered Party'),('S','Sponserer')])
    submit = SubmitField('Login')

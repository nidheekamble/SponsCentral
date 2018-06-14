from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError
from SponsCentral.models import User, PartyUser, SponsorUser,Region

class SelectForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    type = RadioField('User Type',choices=[('P','Sponsored Party'),('S','Sponsor')])
    submit = SubmitField('Proceed')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Tha email is taken. Please choose a different one.')


class RegistrationFormParty(FlaskForm):
    party_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)] )
    party_choices = [('T','Technical'),('S', 'Sports'),('C', 'Cultural')]#add "others"
    party_type = SelectField('Type', choices=party_choices, validators=[Required()])
    party_kind = SelectField('Accepting', choices=[('C','Cash'), ('k','Kind')], validators=[Required()])
    party_contactNo1 = IntegerField('Contact No.1', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    party_contactNo2 = IntegerField('Contact No.2', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    party_address = TextAreaField('Address', validators=[DataRequired()])
    party_about = TextAreaField('About Your Organization', validators=[DataRequired()] )
    party_fromAmount = IntegerField('From Amount', validators=[DataRequired()])
    party_toAmount = IntegerField('To Amount', validators=[DataRequired()])
    party_submit = SubmitField('Sign Up')
    party_logo = FileField('Logo',validators=[FileAllowed(['jpg', 'png'])])#put validators

    def validate_party_name(self, party_name):
        partyUser = PartyUser.query.filter_by(party_name=party_name.data).first()
        if partyUser:
            raise ValidationError('That Name is taken. Please choose a different one.')

    def validate_party_contactNo1(self, party_contactNo1):
        partyUser = PartyUser.query.filter_by(party_contactNo1=party_contactNo1.data).first()
        if partyUser:
            raise ValidationError('Your primary Contact No. is already registered. Please choose a different one.')

    def validate_party_contactNo2(self, party_contactNo2):
        partyUser = PartyUser.query.filter_by(party_contactNo2=party_contactNo2.data).first()
        if partyUser:
            raise ValidationError('Your secondary Contact No. is registered. Please choose a different one.')

    def validate_party_address(self, party_address):
        partyUser = PartyUser.query.filter_by(party_address=party_address.data).first()
        if partyUser:
            raise ValidationError('The Address is already registered. Please choose a different one.')


class RegistrationFormSponser(FlaskForm):
    sponsor_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)] )
    sponsor_choices = [('F','Finance'),('IT','Information Technology'),('O','Others')]#add "others"
    sponsor_type = SelectField('Type Of Sponser', choices=sponsor_choices, validators=[Required()])
    sponsor_kind = SelectField('Offering', choices=[('C','Cash'), ('k','Kind')], validators=[Required()])
    sponsor_contactNo1 = IntegerField('Contact No.1', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    sponsor_contactNo2 = IntegerField('Contact No.2', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    sponsor_address = TextAreaField('Address', validators=[DataRequired()])
    sponsor_about = TextAreaField('About Your Organization', validators=[DataRequired()])
    sponsor_fromAmount = IntegerField('From Amount', validators=[Required()])
    sponsor_toAmount = IntegerField('To Amount', validators=[Required()])
    sponsor_submit = SubmitField('Sign Up')
    sponsor_logo = FileField('Logo',validators=[FileAllowed(['jpg', 'png'])])#put validators


    def validate_sponsor_name(self, sponsor_name):
        sponsorUser = SponsorUser.query.filter_by(sponsor_name=sponsor_name.data).first()
        if sponsorUser:
            raise ValidationError('That Name is taken. Please choose a different one.')

    def validate_sponsor_contactNo1(self, sponsor_contactNo1):
        sponsorUser = SponsorUser.query.filter_by(sponsor_contactNo1=sponsor_contactNo1.data).first()
        if sponsorUser:
            raise ValidationError('Your primary Contact No. is already registered. Please choose a different one.')

    def validate_sponsor_contactNo2(self, sponsor_contactNo2):
        sponsorUser = SponsorUser.query.filter_by(sponsor_contactNo2=sponsor_contactNo2.data).first()
        if sponsorUser:
            raise ValidationError('Your secondary Contact No. is registered. Please choose a different one.')

    def validate_sponsor_address(self, sponsor_address):
        sponsorUser = SponsorUser.query.filter_by(sponsor_address=sponsor_address.data).first()
        if sponsorUser:
            raise ValidationError('The Address is already registered. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ChatBoxText(FlaskForm):
    #partyUser = PartyUser.query.filter_by(user_id=current_user.id).first()
    text = StringField('Enter Text', validators=[DataRequired(), Length(min=1, max=500)])
    send = SubmitField('Send')

class RequestForm(FlaskForm):
    accepted = HiddenField()
    
    accept= SubmitField('Accept')
    decline = SubmitField('Decline')

class InviteForm(FlaskForm):
    user2_id = HiddenField()
    send = SubmitField('Send')

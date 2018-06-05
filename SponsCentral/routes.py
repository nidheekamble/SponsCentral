from SponsCentral import app, db
from flask import render_template, url_for, flash, redirect
from SponsCentral.forms import RegistrationFormParty, RegistrationFormSponser, LoginForm, SelectForm
from SponsCentral.models import PartyUser, SponsorUser, User
from Crypto.Hash import SHA256 #using PyCrypto functions for hashing


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form= SelectForm()
    if form.validate_on_submit():

        if form.select.data == 'P':

            hash = SHA256.new() #object for PyCrypto SHA2
            hash.update(form.password.data) #update feeds inputs into the function
            hashed_password = hash.digest() #another name for hash value
            user = User( email= form.email.data , password= hashed_password, type= form.select.data )
            db.session.add(user)
            db.session.commit()
            flash(f'Success! Please fill in the remaining details', 'success')
            return redirect(url_for('registerParty'))

        elif form.select.data == 'S':

            hash = SHA256.new()
            hash.update(form.password.data)
            hashed_password = hash.digest()
            user = user(email=form.email.data, password=hashed_password, type= form.select.data )
            db.session.add(user)
            db.session.commit()
            flash(f'Success! Please fill in the remaining details', 'success')
            return redirect(url_for('registerSponsor'))
    else: print('halaaaa')
    return render_template('selectForm.html', form=form)


@app.route("/register_party", methods=['GET', 'POST'])
def registerParty():
    form = RegistrationFormParty()
    if form.validate_on_submit():
        partyUser=PartyUser(party_name=form.party_name.data,party_type=form.party_type.data,party_kind=form.party_kind.data,party_contactNo1=form.party_contactNo1.data,party_contactNo2=form.party_contactNo2.data,party_address=form.party_address.data,party_about=form.party_about.data,party_fromAmount=form.party_fromAmount.data ,party_toAmount=form.party_toAmount.data)
        db.session.add(partyUser)
        db.session.commit()
    return render_template('regParty.html', form=form)


@app.route("/register_sponsor", methods=['GET', 'POST'])
def registerSponsor():
    form = RegistrationFormSponser()
    if form.validate_on_submit():
        sponsoruser=SponsorUser(sponsor_name=form.sponsor_name.data,sponsor_type=form.sponsor_type.data,sponsor_kind=form.sponsor_kind.data,sponsor_contactNo1=form.party_contactNo1.data,party_contactNo2=form.sponsor_contactNo2.data,sponsor_address=form.sponsor_address.data, sponsor_about=form.sponsor_about.data,sponsor_fromAmount=form.sponsor_fromAmount.data ,sponsor_toAmount=form.sponsor_toAmount.data)
        db.session.add(sponsoruser)
        db.session.commit()
    return render_template('regSponsor.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

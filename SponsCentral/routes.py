import os
import secrets
from SponsCentral import app, db, bcrypt
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from SponsCentral.forms import RegistrationFormParty, RegistrationFormSponser, LoginForm, SelectForm
from SponsCentral.models import PartyUser, SponsorUser, User
import hashlib #for SHA512
from flask_login import login_user, current_user, logout_user, login_required




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
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        if form.type.data == 'P':
            if form.validate_on_submit():
                #pw = (form.password.data)
                #s = 0
                #for char in pw:
                #    a = ord(char) #ASCII
                #    s = s+a #sum of ASCIIs acts as the salt
                #hashed_password = (str)(hashlib.sha512(((str(s)).encode('utf-8'))+((form.password.data).encode('utf-8'))).hexdigest())

                #SHA512 is has been confirmed to have been working properly for registration and login both.

                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User( email= form.email.data , password= hashed_password, type= form.type.data )
                db.session.add(user)
                db.session.commit()
                flash(f'Success! Please fill in the remaining details', 'success')
            return redirect(url_for('registerParty'))

        elif form.type.data == 'S':
            if form.validate_on_submit():
                #pw = (form.password.data)
                #s = 0
                #for char in pw:
                #   a = ord(char) #ASCII
                #   s = s+a #sum of ASCIIs acts as the salt
                #hashed_password = (str)(hashlib.sha512(((str(s)).encode('utf-8'))+((form.password.data).encode('utf-8'))).hexdigest())
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(email=form.email.data, password=hashed_password, type= form.type.data )
                db.session.add(user)
                db.session.commit()
                flash(f'Success! Please fill in the remaining details', 'success')
            return redirect(url_for('registerSponsor'))
    else: print('halaaaa')
    return render_template('selectForm.html', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/register_party", methods=['GET', 'POST'])
def registerParty():
    form = RegistrationFormParty()
    if form.validate_on_submit():
        partyUser=PartyUser(party_name=form.party_name.data,party_type=form.party_type.data,party_kind=form.party_kind.data,party_contactNo1=form.party_contactNo1.data,party_contactNo2=form.party_contactNo2.data,party_address=form.party_address.data,party_about=form.party_about.data,party_fromAmount=form.party_fromAmount.data ,party_toAmount=form.party_toAmount.data)
        if form.party_logo.data:
            picture_file = save_picture(form.party_logo.data)
            partyUser.party_logo = picture_file
        db.session.add(partyUser)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        party_logo = url_for('static', filename='profile_pics/' + partyUser.party_logo)
        return redirect(url_for('login'))
    return render_template('regParty.html', form=form)


@app.route("/register_sponsor", methods=['GET', 'POST'])
def registerSponsor():
    form = RegistrationFormSponser()
    if form.validate_on_submit():
        sponsorUser=SponsorUser(sponsor_name=form.sponsor_name.data,sponsor_type=form.sponsor_type.data,sponsor_kind=form.sponsor_kind.data,sponsor_contactNo1=form.sponsor_contactNo1.data,sponsor_contactNo2=form.sponsor_contactNo2.data,sponsor_address=form.sponsor_address.data, sponsor_about=form.sponsor_about.data,sponsor_fromAmount=form.sponsor_fromAmount.data ,sponsor_toAmount=form.sponsor_toAmount.data)
        if form.sponsor_logo.data:
            picture_file = save_picture(form.sponsor_logo.data)
            sponsorUser.sponsor_logo = picture_file
        db.session.add(sponsorUser)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        sponsor_logo = url_for('static', filename='profile_pics/' + sponsorUser.sponsor_logo)
        return redirect(url_for('login'))
    return render_template('regSponsor.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #modified to use SHA512

        #s = 0
        #for char in (form.password.data):
        #    a = ord(char)
        #    s = s+a
        #now_hash = (str)((hashlib.sha512(((str(s)).encode('utf-8'))+((form.password.data).encode('utf-8'))).hexdigest())
        if user and bcrypt.check_password_hash(user.password, form.password.data):
        #if user and  user.password==now_hash :


            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            print('halaaa2')
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print('halaaa2')
    else:
        print('halaaa1')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

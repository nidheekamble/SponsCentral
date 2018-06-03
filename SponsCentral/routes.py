from SponsCentral import app
from flask import render_template, url_for, flash, redirect
from SponsCentral.forms import RegistrationFormParty, RegistrationFormSponser, LoginForm, SelectForm
from SponsCentral.models import PartyUser, SponsorUser

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
            return redirect(url_for('register_party'))

        elif form.select.data == 'S':
            return redirect(url_for('register_sponsor'))
    return render_template('selectForm.html', form=form)


@app.route("/register_party", methods=['GET', 'POST'])
def registerParty():
    form = RegistrationFormParty()
    return render_template('regParty.html', form=form)


@app.route("/register_sponsor", methods=['GET', 'POST'])
def registerSponsor():
    form = RegistrationFormSponsor()
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

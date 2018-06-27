import os
import secrets
from SponsCentral import app, db, bcrypt
from PIL import Image
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from SponsCentral.forms import RegistrationFormParty, RegistrationFormSponser, LoginForm, SelectForm,UpdateAccountForm, ChatBoxText, RequestForm, InviteForm
from SponsCentral.models import PartyUser, SponsorUser, User, Region, Conversing, Conversation
import hashlib #for SHA512
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import Session
from math import sqrt
#from googlemaps import Client as GoogleMaps
import requests
from geopy.geocoders import Nominatim
from sqlalchemy import or_

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form= SelectForm(request.form)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        if form.type.data == 'P':
            if form.validate_on_submit():
                pw = (form.password.data)
                s = 0
                for char in pw:
                    a = ord(char) #ASCII
                    s = s+a #sum of ASCIIs acts as the salt
                hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())

                #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User( email= form.email.data , password= hashed_password, type= form.type.data )
                db.session.add(user)
                db.session.commit()
                flash(f'Success! Please fill in the remaining details', 'success')
            return redirect(url_for('registerParty'))

        elif form.type.data == 'S':
            if form.validate_on_submit():
                pw = (form.password.data)
                s = 0
                for char in pw:
                   a = ord(char) #ASCII
                   s = s+a #sum of ASCIIs acts as the salt
                hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
                #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
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
        user = User.query.all().pop()
        partyUser=PartyUser(party_name=form.party_name.data,party_type=form.party_type.data,party_kind=form.party_kind.data,party_contactNo1=form.party_contactNo1.data,party_contactNo2=form.party_contactNo2.data,party_address=form.party_address.data,party_about=form.party_about.data,party_fromAmount=form.party_fromAmount.data ,party_toAmount=form.party_toAmount.data, user_id=user.id)


        geolocator = Nominatim()
        location = geolocator.geocode(partyUser.party_address)
        partyUser.party_latitude = location.latitude
        partyUser.party_longitude = location.longitude

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
        user = User.query.all().pop()
        sponsorUser=SponsorUser(sponsor_name=form.sponsor_name.data,sponsor_type=form.sponsor_type.data,sponsor_kind=form.sponsor_kind.data,sponsor_contactNo1=form.sponsor_contactNo1.data,sponsor_contactNo2=form.sponsor_contactNo2.data,sponsor_address=form.sponsor_address.data, sponsor_about=form.sponsor_about.data,sponsor_fromAmount=form.sponsor_fromAmount.data ,sponsor_toAmount=form.sponsor_toAmount.data, user_id=user.id)

        geolocator = Nominatim()
        location = geolocator.geocode(sponsorUser.sponsor_address)
        sponsorUser.sponsor_latitude = location.latitude
        sponsorUser.sponsor_longitude = location.longitude

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
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        #modified to use SHA512

        s = 0
        for char in (form.password.data):
            a = ord(char)
            s = s+a
        now_hash = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if (user and (user.password==now_hash)):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))

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


@app.route("/account", methods= ['POST', 'GET'])
@login_required
def account():
    if current_user.type == 'P':

        form = UpdateAccountForm()
        partyUser = PartyUser.query.filter_by(user_id=current_user.id).first()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                partyUser.party_logo = picture_file
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.email.data = current_user.email
        party_logo = url_for('static', filename='profile_pics/' + partyUser.party_logo)
        return render_template('accountParty.html', title='Account',party_logo=party_logo, form=form)

    elif current_user.type == 'S':
        form = UpdateAccountForm()
        sponsorUser=SponsorUser.query.filter_by(user_id=current_user.id).first()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                sponsorUser.sponsor_logo = picture_file
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.email.data = current_user.email
        sponsor_logo = url_for('static', filename='profile_pics/' + sponsorUser.sponsor_logo)
        return render_template('accountSponsor.html', title='Account',sponsor_logo=sponsor_logo, form=form)



def nearbyPartyFunc():

    sponsorUser = SponsorUser.query.filter_by(user_id= current_user.id).first()

    lat = sponsorUser.sponsor_latitude
    lng = sponsorUser.sponsor_longitude

    extent = 6000 #radius distance in meters, centered at sponsor address

    list_parties = []
    for party in PartyUser.query.all():
        list_parties.append(party)

    party_data = []
    nearbyParties = []

    for party in list_parties:
        if sqrt(((party.party_latitude - lat) ** 2) + ((party.party_longitude - lng) ** 2)) < extent:
            party_data = [party.party_name, party.party_latitude, party.party_longitude, party.party_address, party.user_id]
            nearbyParties.append(party_data)

    elements = len(nearbyParties)
    return nearbyParties, lat, lng, elements




def nearbySponsorFunc():

    partyUser = PartyUser.query.filter_by(user_id= current_user.id).first()

    lat = partyUser.party_latitude
    lng = partyUser.party_longitude

    extent = 6000 #radius distance in meters, centered at party address

    list_sponsors = []
    for sponsor in SponsorUser.query.all():
        list_sponsors.append(sponsor)

    sponsor_data = []
    nearbySponsors = []

    for sponsor in list_sponsors:
        if sqrt(((sponsor.sponsor_latitude - lat) ** 2) + ((sponsor.sponsor_longitude - lng) ** 2)) < extent:
            sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id]
            nearbySponsors.append(sponsor_data)

    elements = len(nearbySponsors)
    return nearbySponsors, lat, lng, elements



@app.route('/nearbyParty', methods = ['GET', 'POST']) #sponsor looking for parties
@login_required

def nearbyPartyRoute():
    nearbyParties, lat, lng, elements = nearbyPartyFunc()
    return render_template('nearList.html', nearby_list = nearbyParties, lat = lat, lng = lng, elements = elements)



@app.route('/nearbySponsor', methods = ['GET','POST']) #parties looking for sponsors
@login_required

def nearbySponsorRoute():
    nearbySponsors, lat, lng, elements = nearbySponsorFunc()
    #print (elements)
    return render_template('nearList.html', nearby_list = nearbySponsors, lat = lat, lng = lng, elements = elements)



@app.route('/banking', methods = ['GET','POST']) #parties looking for sponsors
@login_required
def banking():
    return render_template('banking.html', title='banking')



@app.route("/requests", methods= ['POST', 'GET'])
@login_required
def inviteRecieved():
    userList=[]
    form = RequestForm()
    conversing = Conversing.query.filter_by(user2d = current_user.id).all()
    print(conversing)
    for user in conversing:
        userList.append(user)
        print(user)
    if form.validate_on_submit():
        if form.accepted.data==0:
            conversing.status="in-touch"
        else:
            conversing.status="Not Accepted"

    return render_template ('requestsPage.html', title = 'requests', form=form, userList=userList)



app.route("/invite", methods= ['POST', 'GET'])
@login_required
def invite():
    form=InviteForm()
    if form.validate_on_submit:
        conversing = Conversing(user1 = current_user.id, user2=form.user2_id.data, status='sent')
        db.session.add(conversing)
        db.session.commit()
    return redirect(url_for('inviteRecieved'))



@app.route("/invites", methods= ['POST', 'GET'])
@login_required
def connection():
    userList=[]
    form = InviteForm()

    if(current_user.type == 'P'):
        for sponsorUser in SponsorUser.query.all():
            userList.append(sponsorUser)

    if(current_user.type == 'S'):
        for partyUser in PartyUser.query.all():
            userList.append(partyUser)

    if form.validate_on_submit:
        conversing = Conversing(user1 = current_user.id, user2 = form.user2_id.data, status='sent')
        print(conversing)
        print(request.form)

        db.session.add(conversing)
        db.session.commit()
    return render_template ('invitesPage.html', title = 'invites', userList=userList, form=form)




@app.route("/chatbox", methods= ['POST', 'GET'])
@login_required
def chatbox():
    conversing= Conversing.query.filter(or_(user1=current_user.id, user2= current_user.id )).all()#just for now
    messages=[""]
    for conversation in Conversation.query.filter_by(conversing_id = conversing.id):#just for now
        messages.append(conversation)
    form = ChatBoxText()
    if form.validate_on_submit():
        conversation= Conversation(text = form.text.data, conversing_id= conversing.id )#just for now
        db.session.add(conversation)
        db.session.commit()
        messages.append(conversation)
    return render_template('chatbox.html', title= 'ChatBox', form=form, messages=messages)

@app.route("/MeetTheTeam")
def team():
    return render_template('MeetTheTeam.html')

@app.route("/WhatWeDo")
def work():
    return render_template('WhatWeDo.html')


@app.route("/user/<user2_id>", methods = ['GET', 'POST'])
@login_required
def user2_account(user2_id):
    if current_user.type == 'P':

        sponsorUser=SponsorUser.query.filter_by(user_id=user2_id).first()
        db.session.commit()
        return render_template('User2Account_sponsor.html', title='Account', sponsorUser=sponsorUser, current_user=current_user)

    elif current_user.type == 'S':

        partyUser = PartyUser.query.filter_by(user_id=user2_id).first()
        db.session.commit()
        return render_template('User2Account_party.html', title='Account', partyUser=partyUser, current_user=current_user)




@app.route("/filterType/<type>", methods = ['GET', 'POST'])
@login_required
def filterType(type):

    if current_user.type == 'P':

        partyUser = PartyUser.query.filter_by(user_id= current_user.id).first()

        lat = partyUser.party_latitude
        lng = partyUser.party_longitude

        nearbySponsors = nearbySponsorFunc()
        filteredList = SponsorUser.query.filter_by(sponsor_type=type).all()
        filteredSponsors = []

        for sponsor in filteredList:
            sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id]
            filteredSponsors.append(sponsor_data)

        elements = len(filteredSponsors)
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements)

    elif current_user.type == 'S':

        sponsorUser = SponsorUser.query.filter_by(user_id=current_user.id).first()

        lat = sponsorUser.sponsor_latitude
        lng = sponsorUser.sponsor_longitude

        nearbyParties = nearbyPartyFunc()
        filteredList = PartyUser.query.filter_by(party_type=type).all()
        filteredParties = []

        for party in filteredList:
            party_data = [party.party_name, party.party_latitude, party.party_longitude, party.party_address, party.user_id]
            filteredParties.append(party_data)

        elements = len(filteredParties)
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements)




@app.route("/filterFrom/<lowerBound>", methods = ['GET', 'POST'], endpoint='filterFrom')
@login_required
def filterFrom(lowerBound):

    if current_user.type == 'P':

        partyUser = PartyUser.query.filter_by(user_id= current_user.id).first()

        lat = partyUser.party_latitude
        lng = partyUser.party_longitude

        nearbySponsors = nearbySponsorFunc()
        filteredList = SponsorUser.query.filter_by(sponsor_fromAmount=lowerBound).all()
        filteredSponsors = []

        for sponsor in filteredList:
            sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id]
            filteredSponsors.append(sponsor_data)

        elements = len(filteredSponsors)
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements)


    elif current_user.type == 'S':

        sponsorUser = SponsorUser.query.filter_by(user_id=current_user.id).first()

        lat = sponsorUser.sponsor_latitude
        lng = sponsorUser.sponsor_longitude

        nearbyParties = nearbyPartyFunc()
        filteredList = PartyUser.query.filter_by(party_fromAmount=lowerBound).all()
        filteredParties = []

        for party in filteredList:
            party_data = [party.party_name, party.party_latitude, party.party_longitude, party.party_address, party.user_id]
            filteredParties.append(party_data)

        elements = len(filteredParties)
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements)




@app.route("/filterTo/<upperBound>", methods = ['GET', 'POST'])
@login_required
def filterTo(upperBound):

    if current_user.type == 'P':

        partyUser = PartyUser.query.filter_by(user_id= current_user.id).first()

        lat = partyUser.party_latitude
        lng = partyUser.party_longitude

        nearbySponsors = nearbySponsorFunc()
        filteredList = SponsorUser.query.filter_by(sponsor_toAmount=upperBound).all()
        filteredSponsors = []

        for sponsor in filteredList:
            sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id]
            filteredSponsors.append(sponsor_data)

        elements = len(filteredSponsors)
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements)


    elif current_user.type == 'S':

        sponsorUser = SponsorUser.query.filter_by(user_id=current_user.id).first()

        lat = sponsorUser.sponsor_latitude
        lng = sponsorUser.sponsor_longitude

        nearbyParties = nearbyPartyFunc()
        filteredList = PartyUser.query.filter_by(party_toAmount=upperBound).all()
        filteredParties = []

        for party in filteredList:
            party_data = [party.party_name, party.party_latitude, party.party_longitude, party.party_address, party.user_id]
            filteredParties.append(party_data)

        elements = len(filteredParties)
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements)




@app.route("/filterKind/<kind>", methods = ['GET', 'POST'])
@login_required
def filterKind(kind):

    if current_user.type == 'P':

        partyUser = PartyUser.query.filter_by(user_id= current_user.id).first()

        lat = partyUser.party_latitude
        lng = partyUser.party_longitude

        nearbySponsors = nearbySponsorFunc()
        filteredList = SponsorUser.query.filter_by(sponsor_kind=kind).all()
        filteredSponsors = []

        for sponsor in filteredList:
            sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id]
            filteredSponsors.append(sponsor_data)

        elements = len(filteredSponsors)
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements)


    elif current_user.type == 'S':

        sponsorUser = SponsorUser.query.filter_by(user_id=current_user.id).first()

        lat = sponsorUser.sponsor_latitude
        lng = sponsorUser.sponsor_longitude

        nearbyParties = nearbyPartyFunc()
        filteredList = PartyUser.query.filter_by(party_kind=kind).all()
        filteredParties = []

        for party in filteredList:
            party_data = [party.party_name, party.party_latitude, party.party_longitude, party.party_address, party.user_id]
            filteredParties.append(party_data)

        elements = len(filteredParties)
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements)

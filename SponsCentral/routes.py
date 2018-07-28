import os
import secrets
from SponsCentral import app, db, bcrypt
from SponsCentral.globalVar import shortlist
from PIL import Image
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from SponsCentral.forms import RegistrationFormParty, RegistrationFormSponser, LoginForm, SelectForm,UpdateAccountFormParty,UpdateAccountFormSponsor, ChatBoxText, RequestForm, InviteForm
from SponsCentral.models import PartyUser, SponsorUser, User, Conversing, Conversation
import hashlib #for SHA512
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import Session
from math import sqrt
#from googlemaps import Client as GoogleMaps
import requests
from geopy.geocoders import Nominatim
from sqlalchemy import or_ , and_

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')



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

        partyUser.party_address.replace('\n',' ')
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

        sponsorUser.sponsor_address.replace('\n',' ')
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
        form = UpdateAccountFormParty()
        partyUser = PartyUser.query.filter_by(user_id=current_user.id).first()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                partyUser.party_logo = picture_file
            current_user.email = form.email.data
            partyUser.party_name=form.party_name.data
            partyUser.party_type=form.party_type.data
            partyUser.party_kind=form.party_kind.data
            partyUser.party_fromAmount=form.party_fromAmount.data
            partyUser.party_toAmount=form.party_toAmount.data
            partyUser.party_about=form.party_about.data
            partyUser.party_address=form.party_address.data
            partyUser.party_contactNo1=form.party_contactNo1.data
            partyUser.party_contactNo2=form.party_contactNo2.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.email.data = current_user.email
            form.party_name.data=partyUser.party_name
            form.party_type.data=partyUser.party_type
            form.party_kind.data=partyUser.party_kind
            form.party_fromAmount.data=partyUser.party_fromAmount
            form.party_toAmount.data=partyUser.party_toAmount
            form.party_about.data=partyUser.party_about
            form.party_address.data=partyUser.party_address
            form.party_contactNo1.data=partyUser.party_contactNo1
            form.party_contactNo2.data=partyUser.party_contactNo2
        party_logo = url_for('static', filename='profile_pics/' + partyUser.party_logo)
        return render_template('accountParty.html', title='Account',party_logo=party_logo, form=form)

    elif current_user.type == 'S':
        form = UpdateAccountFormSponsor()
        sponsorUser=SponsorUser.query.filter_by(user_id=current_user.id).first()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                sponsorUser.sponsor_logo = picture_file
            current_user.email = form.email.data
            sponsorUser.sponsor_name=form.sponsor_name.data
            sponsorUser.sponsor_type=form.sponsor_type.data
            sponsorUser.sponsor_kind=form.sponsor_kind.data
            sponsorUser.sponsor_fromAmount=form.sponsor_fromAmount.data
            sponsorUser.sponsor_toAmount=form.sponsor_toAmount.data
            sponsorUser.sponsor_about=form.sponsor_about.data
            sponsorUser.sponsor_address=form.sponsor_address.data
            sponsorUser.sponsor_contactNo1=form.sponsor_contactNo1.data
            sponsorUser.sponsor_contactNo2=form.sponsor_contactNo2.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.email.data = current_user.email
            form.sponsor_name.data=sponsorUser.sponsor_name
            form.sponsor_type.data=sponsorUser.sponsor_type
            form.sponsor_kind.data=sponsorUser.sponsor_kind
            form.sponsor_fromAmount.data=sponsorUser.sponsor_fromAmount
            form.sponsor_toAmount.data=sponsorUser.sponsor_toAmount
            form.sponsor_about.data=sponsorUser.sponsor_about
            form.sponsor_address.data=sponsorUser.sponsor_address
            form.sponsor_contactNo1.data=sponsorUser.sponsor_contactNo1
            form.sponsor_contactNo2.data=sponsorUser.sponsor_contactNo2
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
        party_data = [party.party_name, party.party_latitude, party.party_longitude, party.party_address, party.user_id, party.party_fromAmount, party.party_toAmount]
        nearbyParties.append(party_data)

    elements = len(nearbyParties)
    return nearbyParties, lat, lng, elements



@app.route('/nearbyParty', methods = ['GET', 'POST']) #sponsor looking for parties
@login_required
def nearbyPartyRoute():
    nearbyParties, lat, lng, elements = nearbyPartyFunc()
    sponsorUser = SponsorUser.query.filter_by(user_id=current_user.id).first()
    return render_template('nearList.html', nearby_list = nearbyParties, lat = lat, lng = lng, elements = elements, sponsorUser = sponsorUser, title = 'Nearby Parties')



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
        sponsor_data = [sponsor.sponsor_name, sponsor.sponsor_latitude, sponsor.sponsor_longitude, sponsor.sponsor_address, sponsor.user_id, sponsor.sponsor_fromAmount, sponsor.sponsor_toAmount]
        nearbySponsors.append(sponsor_data)

    elements = len(nearbySponsors)
    return nearbySponsors, lat, lng, elements





@app.route('/nearbySponsor', methods = ['GET','POST']) #parties looking for sponsors
@login_required
def nearbySponsorRoute():
    nearbySponsors, lat, lng, elements = nearbySponsorFunc()
    partyUser = PartyUser.query.filter_by(user_id=current_user.id).first()
    return render_template('nearList.html', nearby_list = nearbySponsors, lat = lat, lng = lng, elements = elements, partyUser = partyUser, title = 'Nearby Sponsor')


@app.route("/user/<user2_id>", methods = ['GET', 'POST'])
@login_required
def user2_account(user2_id):

    conversing=Conversing.query.filter(and_(Conversing.user1==current_user.id,Conversing.user2==user2_id)).first()
    if conversing==None:

        if current_user.type == 'P':

            form=InviteForm()
            sponsorUser=SponsorUser.query.filter_by(user_id=user2_id).first()
            user = User.query.filter_by(id  = sponsorUser.user_id).first()
            flag=1
            if form.validate_on_submit():
                conversing=Conversing(user1=current_user.id,user2=user2_id,status='Sent')
                db.session.add(conversing)
                db.session.commit()

            return render_template('User2Account_sponsor.html', title='Account', sponsorUser=sponsorUser,user = user,form=form,flag=flag)

        elif current_user.type == 'S':

            form=InviteForm()
            partyUser = PartyUser.query.filter_by(user_id=user2_id).first()
            user = User.query.filter_by(id  = partyUser.user_id).first()
            flag=1
            if form.validate_on_submit():
                conversing=Conversing(user1=current_user.id,user2=user2_id,status='Sent')
                db.session.add(conversing)
                db.session.commit()

            return render_template('User2Account_party.html', title='Account', partyUser=partyUser, user = user,form=form,flag=flag)

    else:
        if current_user.type == 'P':
            flag=0
            sponsorUser=SponsorUser.query.filter_by(user_id=user2_id).first()
            user = User.query.filter_by(id  = sponsorUser.user_id).first()

            return render_template('User2Account_sponsor.html', title='Account', sponsorUser=sponsorUser, user = user,flag=flag)

        elif current_user.type == 'S':
            flag=0
            partyUser = PartyUser.query.filter_by(user_id=user2_id).first()
            user = User.query.filter_by(id  = partyUser.user_id).first()

            return render_template('User2Account_party.html', title='Account', partyUser=partyUser, user = user,flag=flag)


@app.route("/requests", methods= ['POST', 'GET'])
@login_required
def inviteRecieved():

    userList=[]
    conversing= Conversing.query.filter(and_(Conversing.status=='Sent',Conversing.user2==current_user.id)).all()
    form = RequestForm()
    print(conversing)
    print(10001)

    if current_user.type == 'S':
        for user in conversing:
            user_invitee=PartyUser.query.filter_by(user_id=user.user1).first()
            #user_name=user_invitee.party_name
            userList.append(user_invitee)
            print(user_invitee.party_name)

            if form.validate_on_submit():
                if form.invite_status.data=='1':
                    user.status='In-touch'
                    db.session.commit()
                elif  form.invite_status.data=='0':
                    user.status='Not Accepted'
                    db.session.commit()
        return render_template ('requestsPageSponsor.html', title = 'requests', form=form, userList=userList)

    if current_user.type == 'P':
        for user in conversing:
            user_invitee=SponsorUser.query.filter_by(user_id=user.user1).first()
            #user_name=user_invitee.sponsor_name
            userList.append(user_invitee)
            print(user_invitee.sponsor_name)

            if form.validate_on_submit():
                if form.invite_status.data=='1':
                    user.status='In-touch'
                    db.session.commit()
                elif  form.invite_status.data=='0':
                    user.status='Not Accepted'
                    db.session.commit()

        return render_template ('requestsPageParty.html', title = 'requests', form=form, userList=userList)



@app.route("/shortlist/<user2_id>", methods= ['POST', 'GET'])
@login_required
def shortlisted(user2_id):

    form = InviteForm()

    if current_user.type == 'S':
        shortlisted_user=PartyUser.query.filter_by(user_id=user2_id).first()

        flag=0
        for partyUser in shortlist:
            if partyUser.user_id == shortlisted_user.user_id:
                flag=1
                print("nahin hua")
                break
        if flag==0:
            shortlist.append(shortlisted_user)
            print("hua")

        print(shortlist)
        #session.expunge(shortlisted_user)
        db.session.commit()
        return render_template ('shortlistPageSponsor.html', title = 'Shortlist', userList=shortlist, form=form)


    elif current_user.type =='P':
        shortlisted_user=SponsorUser.query.filter_by(user_id=user2_id).first()

        flag=0
        for sponsorUser in shortlist:
            if sponsorUser.user_id == shortlisted_user.user_id:
                flag=1
                print("nahin hua")
                break
        if flag==0:
            shortlist.append(shortlisted_user)
            print("hua")

        print(shortlist)
        #session.expunge(shortlisted_user)
        db.session.commit()
        return render_template ('shortlistPageParty.html', title = 'Shortlist', userList=shortlist, form=form)



@app.route("/display_shortlist", methods = ['GET','POST'])
@login_required
def display_shortlist():

	form = InviteForm()

	if current_user.type == 'S':
		return render_template ('shortlistPageSponsor.html', title = 'Shortlist', userList=shortlist, form=form)

	elif current_user.type == 'P':
		return render_template ('shortlistPageParty.html', title = 'Shortlist', userList=shortlist, form=form)



@app.route("/individual_address/<otherUser_id>", methods = ['GET', 'POST'])
@login_required
def individual_address(otherUser_id):

    if current_user.type == 'P':
        partyUser = PartyUser.query.filter_by(user_id= current_user.id).first()
        lat = partyUser.party_latitude
        lng = partyUser.party_longitude

        otherUser = SponsorUser.query.filter_by(user_id=otherUser_id).first()
        lat2 = otherUser.sponsor_latitude
        lng2 = otherUser.sponsor_longitude

    elif current_user.type == 'S':

        sponsorUser = SponsorUser.query.filter_by(user_id= current_user.id).first()
        lat = sponsorUser.sponsor_latitude
        lng = sponsorUser.sponsor_longitude

        otherUser = PartyUser.query.filter_by(user_id=otherUser_id).first()
        lat2 = otherUser.party_latitude
        lng2 = otherUser.party_longitude

    return render_template ('API.html', title = 'Compare Your Location', lat=lat, lng=lng, lat2=lat2, lng2=lng2, current_user=current_user)



@app.route("/chatwith", methods= ['POST', 'GET'])#Whom do you want to chat with?
@login_required
def chatwith():
    associated_users_list=[]
    conversing= Conversing.query.filter(or_(Conversing.user1==current_user.id,Conversing.user2==current_user.id)).all()
    conversing2= Conversing.query.filter(or_(Conversing.user1==current_user.id,Conversing.user2==current_user.id)).first()


    if conversing2 == None:
        print('10001')
        return render_template ('chatError.html', title = 'Chat Error',current_user=current_user)
    else:
        for nowuser in conversing :
            print('1000')
            print(nowuser.status)
            if nowuser.user1== current_user.id:
                if nowuser.status=='In-touch':
                    if current_user.type == 'P':
                        sponsorUser= SponsorUser.query.filter_by(user_id=nowuser.user2).first()
                        associated_user=[sponsorUser.user_id,sponsorUser.sponsor_name]
                        associated_users_list.append(associated_user)
                    elif current_user.type == 'S':
                        partyUser= PartyUser.query.filter_by(user_id=nowuser.user2).first()
                        associated_user=[partyUser.user_id,partyUser.party_name]
                        associated_users_list.append(associated_user)
            elif nowuser.user2== current_user.id:
                if nowuser.status=='In-touch':
                    if current_user.type == 'P':
                        sponsorUser= SponsorUser.query.filter_by(user_id=nowuser.user1).first()
                        associated_user=[sponsorUser.user_id,sponsorUser.sponsor_name]
                        associated_users_list.append(associated_user)
                    elif current_user.type == 'S':
                        partyUser= PartyUser.query.filter_by(user_id=nowuser.user1).first()
                        associated_user=[partyUser.user_id,partyUser.party_name]
                        associated_users_list.append(associated_user)
        if associated_users_list==[]:
            return render_template ('chatError.html', title = 'No Users')
        return render_template ('chatlist.html', title = 'Chat with', associated_users_list=associated_users_list)



    #return associated_users_choices
@app.route("/chatbox/<chatwith_id>", methods= ['POST', 'GET'])#Whom do you want to chat with?
@login_required
def chat(chatwith_id):
    print(chatwith_id)
    form=ChatBoxText()
    messages=[]
    conversing= Conversing.query.filter(or_(Conversing.user1==chatwith_id,Conversing.user2==chatwith_id)).all()
    for nowuser in conversing:
        if current_user.type=='P':
            if nowuser.user1== current_user.id:

                user=SponsorUser.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.sponsor_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]
                    messages.append(message)

            elif  nowuser.user2==current_user.id:
                user=SponsorUser.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.sponsor_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]#just for now
                    messages.append(message)

        elif current_user.type=='S':
            if nowuser.user1== current_user.id :
                user=PartyUser.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.party_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]
                    messages.append(message)

            elif nowuser.user2==current_user.id :
                user=PartyUser.query.filter_by(user_id=chatwith_id).first()
                messages=[[user.party_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                        #partyUser=PartyUser.query.filter_by(user_id=chatwith_id).first()#just for now
                    message=[conversation.text,conversation.time, conversation.sender_id]
                    messages.append(message)

    return render_template('chatbox.html', title= 'ChatBox', form=form, messages=messages, current_user=current_user, user=user)




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
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements, partyUser = partyUser)

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
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements, sponsorUser = sponsorUser)




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
        return render_template('nearList.html', nearby_list = filteredSponsors, lat = lat, lng = lng, elements = elements, partyUser = partyUser)


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
        return render_template('nearList.html', nearby_list = filteredParties, lat = lat, lng = lng, elements = elements, sponsorUser = sponsorUser)



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/MeetTheTeam")
def team():
    return render_template('MeetTheTeam.html')

@app.route("/WhatWeDo")
def work():
    return render_template('WhatWeDo.html')


@app.route('/banking', methods = ['GET','POST']) #parties looking for sponsors
@login_required
def banking():
    return render_template('banking.html', title='Banking')


@app.route('/email', methods = ['GET', 'POST'])
@login_required
def email():
    return render_template('email.html', title='Email')

from flask import Flask, session, redirect, url_for, escape, request
from math import sqrt
from googlemaps import GoogleMaps

app = Flask(__name__)
app.secret_key = '42755hfn'

gmaps = GoogleMaps("AIzaSyCZShSU-ew_wZxGfZcPB8IkyLDq1FuSE0Q") #API key

@app.route('/nearbyparty', methods = 'POST') #sponsor looking for parties
def nearbyparty():

	form = request.form()
	location = form.sponsor_address.data
	lat, lng = gmaps.address_to_latlng(location) #converting string address to coordinates

	extent = 3000 #radius distance in meters, centered at user address

	list_Parties = PartyUser.query.all()
	nearbyParties = []
	for party in list_Parties:
		if sqrt((party.party_latitude - lat ** 2) + (party.party_longitude - lng) ** 2) < extent:
	        nearby_Parties.append(party.__dict__)

    return flask.jsonify(list_Parties) #returns the filtered list



@app.route('/nearbysponsor', methods = 'POST') #parties looking for sponsors
def nearbysponsor():
	form = request.form()
	location = form.party_address.data
	lat, lng = gmaps.address_to_latlng(location)

	list_Sponsor = SponsorUser.query.all()
	nearby_Sponsor = []
	for sponsor in list_Sponsor:
		if sqrt((sponsor.sponsor_latitude - lat ** 2) + (sponsor.sponsor_longitude - lng) ** 2) < extent:
	        nearby_Sponsor.append(sponsor.__dict__)

    return flask.jsonify(list_Sponsor)

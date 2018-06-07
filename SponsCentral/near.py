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

	listp = PartyUser.query.all()
	nearp = []
	for party in listp:
		if sqrt((party.party_latitude - lat ** 2) + (party.party_longitude - lng) ** 2) < extent:
	        listp.append(party.__dict__)

    return flask.jsonify(listp) #returns the filtered list



@app.route('/nearbysponsor', methods = 'POST') #parties looking for sponsors
def nearbysponsor():
	form = request.form()
	location = form.party_address.data
	lat, lng = gmaps.address_to_latlng(location)

	lists = SponsorUser.query.all()
	nears = []
	for sponsor in lists:
		if sqrt((sponsor.sponsor_latitude - lat ** 2) + (sponsor.sponsor_longitude - lng) ** 2) < extent:
	        lists.append(sponsor.__dict__)

    return flask.jsonify(lists)

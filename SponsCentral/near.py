from flask import Flask, session, redirect, url_for, escape, request
from math import sqrt
from flask_login import login_user, current_user, logout_user, login_required
from googlemaps import Client as GoogleMaps
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.secret_key = '42755hfn'

gmaps = GoogleMaps("AIzaSyCQP9mlZC1VIO7J5J5wZensClSVDfDSfxE") #API key for geocoding

#url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=lat,lng&destinations=region.latitude,region.longitude&key=AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA'
# r = requests.get(url, data=None)
#API key for Matrix API

@app.route('/nearbyParty', methods = ['POST']) #sponsor looking for parties
@login_required

def nearbyParty():

	geolocator = Nominatim()
    location = geolocator.geocode(sponsorUser.sponsor_address)
    lat = location.latitude
    lng = location.longitude #converting string address to coordinates


	'''extent = 2000 #radius distance in meters, centered at sponsor address

	list_Regions = []
	list_Regions = Region.query.all()
	nearbyRegion = [] #finding regions nearest to sponsor

	for reg in list_Regions:
		if sqrt((reg.latitude - lat ** 2) + (reg.longitude - lng) ** 2) < extent:
				nearbyRegion.append(reg.__dict__)

	list_Parties = []
	list_Parties = PartyUser.query.all()
	partyNearRegion = [] #finding parties in/near each of the close regions
	for party in list_Parties:
		for reg in nearbyRegion: 
			if sqrt(((party.party_latitude - reg.latitude) ** 2) + ((party.party_longitude - reg.longitude) ** 2)) < extent:
				partyNearRegion.append(party.__dict__)


	nearbyParty = [] #final filter for further selecting those parties close to the sponsor

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':partyNearRegion,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)
	if(r.json()<extent):
		nearbyParty.append(party.__dict__)
	#print(r.json())
	return flask.jsonify(nearbyParty)'''

	list_Parties = []
	list_Parties = PartyUser.query.all()
	destinations = [str(party.party_latitude)+','+str(party.party_longitude) for party in list_Parties]
	destinations = '|'.join(destinations)

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':destinations,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)
	return(r.json())



@app.route('/nearbySponsor', methods = ['POST']) #parties looking for sponsors
@login_required

def nearbySponsor():

	geolocator = Nominatim()
    location = geolocator.geocode(partyUser.party_address)
    lat = location.latitude
    lng = location.longitude

	'''extent = 2000 #radius distance in meters, centered at party address

	list_Regions = []
	list_Regions = Region.query.all()
	nearbyRegion = [] #finding regions nearest to party

	for reg in list_Regions:
		if sqrt((reg.latitude - lat ** 2) + (reg.longitude - lng) ** 2) < extent:
				nearbyRegion.append(reg.__dict__)

	list_Sponsors = []
	list_Sponsors = SponsorUser.query.all()
	sponsorNearRegion = [] #finding Sponsors in/near each of the close regions
	for sponsor in list_Sponsors:
		for reg in nearbyRegion:
			if sqrt(((sponsor.sponsor_latitude - reg.latitude) ** 2) + ((sponsor.sponsor_longitude - reg.longitude) ** 2)) < extent:
				sponsorNearRegion.append(sponsor.__dict__)


	nearbySponsor = [] #final filter for further selecting those Sponsors close to the party

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':sponsorNearRegion,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)
	if(r.json()<extent):
		nearbySponsor.append(sponsor.__dict__)
	#print(r.json())
	return flask.jsonify(nearbySponsor)'''

	list_Sponsors = []
	list_Sponsors = PartyUser.query.all()
	destinations = [str(sponsor.sponsor_latitude)+','+str(sponsor.sponsor_longitude) for sponsor in list_Parties]
	destinations = '|'.join(destinations)

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':destinations,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)
	return(r.json())

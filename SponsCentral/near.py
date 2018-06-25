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

	lat = sponsorUser.sponsor_latitude
	lng = sponsorUser.sponsor_longitude

	'''extent = 2000 #radius distance in meters, centered at sponsor address

	list_regions = []
	for region in Region.query.all():
		list_regions.append()

	nearbyRegion = [] #finding regions nearest to sponsor

	for region in list_regions:
		if sqrt(((region.latitude - lat)** 2) + ((region.longitude - lng) ** 2)) < extent:
				nearbyRegion.append(region.__dict__)

	list_parties = []
	for party in PartyUser.query.all():
		list_parties.append()

	partyNearRegion = [] #finding parties in/near each of the close regions

	for party in list_parties:
		for region in nearbyRegion: 
			if sqrt(((party.party_latitude - region.latitude) ** 2) + ((party.party_longitude - region.longitude) ** 2)) < extent:
				partyNearRegion.append(party.__dict__)


	for party in partyNearRegion:
		destinations = [str(party.party_latitude)+','+str(party.party_longitude)]
		if sqrt(((party.party_latitude - lat) ** 2) + ((party.party_longitude - lng) ** 2)) < extent:
			destinations = '|'.join(destinations)

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':destinations,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)

	return(r.json())
	'''

	list_parties = []
	for party in PartyUser.query.all():
		list_parties.append()

	destinations = [str(party.party_latitude)+','+str(party.party_longitude) for party in list_parties]
	destinations = '|'.join(destinations)

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':destinations,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)

	return(r.json())



@app.route('/nearbySponsor', methods = ['POST']) #parties looking for sponsors
@login_required

def nearbySponsor():

	lat = partyUser.party_latitude
	lng = partyUser.party_longitude

	'''extent = 2000 #radius distance in meters, centered at party address

	list_regions = []
	for region in Region.query.all():
		list_regions.append()

	nearbyRegion = [] #finding regions nearest to sponsor

	for region in list_regions:
		if sqrt(((region.latitude - lat)** 2) + ((region.longitude - lng) ** 2)) < extent:
				nearbyRegion.append(region.__dict__)

	list_sponsors = []
	for sponsor in SponsorUser.query.all():
		list_sponsors.append()

	sponsorNearRegion = [] #finding sponsors in/near each of the close regions

	for sponsor in list_sponsors:
		for region in nearbyRegion:
			if sqrt(((sponsor.sponsor_latitude - region.latitude) ** 2) + ((sponsor.sponsor_longitude - region.longitude) ** 2)) < extent:
				sponsorNearRegion.append(sponsor.__dict__)


	for sponsor in sponsorNearRegion:
		destinations = [str(sponsor.sponsor_latitude)+','+str(sponsor.sponsor_longitude)]
		if sqrt(((sponsor.sponsor_latitude - lat) ** 2) + ((sponsor.sponsor_longitude - lng) ** 2)) < extent:
			destinations = '|'.join(destinations)

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':destinations,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)

	return(r.json())'''

	list_sponsors = []
	for sponsor in SponsorUser.query.all():
		list_sponsors.append()

	destinations = [str(sponsor.sponsor_latitude)+','+str(sponsor.sponsor_longitude) for sponsor in list_sponsors]
	destinations = '|'.join(destinations)

	PARAMS = {'units': imperial,'origins':(lat,lng),'destinations':destinations,'key':AIzaSyBGpPXl5E1bWDxU6vaU7BZm8JKWWasGzCA} #API key for matrix API
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' #API key for matrix API
	r = requests.get(url, params=PARAMS)

	return(r.json())

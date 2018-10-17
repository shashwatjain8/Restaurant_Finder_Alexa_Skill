#!/usr/bin/env python
from flask import Flask
from flask_ask import Ask, statement, question, session
from flask import Flask
from flask import request
from flask import jsonify
import requests
from bs4 import BeautifulSoup

import geocoder
import json


app = Flask(__name__)
ask = Ask(app, '/restaurantfinder')

Zomatokey='501bbf545d951052f8777581b5750dcd'


def sendnear(lat , lon):
    baseurl='https://developers.zomato.com/api/v2.1/geocode?lat=%f&lon=%f' %(lat,lon)
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "501bbf545d951052f8777581b5750dcd"}
    response = requests.get(baseurl, headers=header)
    g=response.json()
    # for x in range(len(g['nearby_restaurants'])):
    #     print g['nearby_restaurants'][x]['restaurant']['name']      
    return g

@app.route('/')
def homepage():
    return 'Welcome to Restaurant Finder'

@ask.launch
def start_skill():
    message = 'Hey..I can tell you some nearby places to dine in..... How many restaurants would you like to know?'
    return question(message)

@ask.intent("NumberIntent",convert = {"number" : int})
def team_intent(number):
	#team = intent['slots']['teamname']
	g = geocoder.ip('me')
	lat = g.latlng[0]
	lon = g.latlng[1]
	g =  sendnear(lat, lon)
	count =0
	message = "Here are some places i could find...."
	for x in range(len(g['nearby_restaurants'])):
		count = count + 1
		message = message + g['nearby_restaurants'][x]['restaurant']['name'] + "....."
		if count == number:
			break
	return statement(message)


@ask.intent("YesIntent")
def yes_Intent():
    message = 'Say a number'
    return question(message)

@ask.intent("NoIntent")
def no_Intent():
    message = 'Well that is fine...Maybe next time'
    return statement(message)

@ask.intent("AMAZON.CancelIntent")
def cancel_Intent():
    message = 'See you again...bye'
    return statement(message)

@ask.intent("AMAZON.StopIntent")
def stop_Intent():
    message = 'See you again...bye'
    return statement(message)

@ask.intent("AMAZON.HelpIntent")
def help_Intent():
    message = 'Say yes to get a list of top 5 near by restaurants..'
    return question(message)

if __name__ == '__main__':
    app.run(threaded = True)
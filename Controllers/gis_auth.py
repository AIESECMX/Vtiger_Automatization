import urllib
import urllib2
import cookielib
import logging
import requests
import json


class GIS:
    
mc  = 1589 #Mexico
date = datetime.datetime.now()
#now = datetime.date(2016,10,3)

    def __init__(self, email, password):
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.email = email
        self.login_data = urllib.urlencode({'user[email]': email, 'user[password]': password})

    def generateCredentials(self):
        self.opener.open('https://auth.aiesec.org/users/sign_in', self.login_data)
        token = None
        for cookie in self.cj:
            if cookie.name == 'expa_token':
                token = cookie.value
        if token is None:
            raise Exception('Unable to generate a token for {0}!'.format(self.email))
        return token

    #gets mcs in expa
    def getMC(self,date):

    #get LCs
    def getLCs(self,date):

    #gets opportunities
    def getOpportunities(self,date):

    #def updates opportunities expecting an array
    def updateOpportunities(self,opportunitys):

    #get application 
    def getApplications(self, date):

    #updates applicacionts expecting an array
    def updateApplications(seld,applications):

    #get enablers
    def getEnablers(self,date):

    #updates enablers expects array
    def updateEnabers(self,enablers):

    #gets people
    def getPeople(seld,date):

    #updates people expects array
    def updatePeople(seld,people):




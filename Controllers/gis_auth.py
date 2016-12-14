import urllib
import urllib2
import cookielib
import logging
import requests
import json
import datetime
import sys
sys.path.insert(0,sys.path[0]+'/../Model')
from LC import LC
from Opportunity import Opportunity
from Application import Application
from Enabler import Enabler
from People import People

class GIS:



    #
    def __init__(self, email, password):
        self.mc = 1589 #Mexico
        #now = datetime.date(2016,10,3)
        self.date = datetime.datetime.now()
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.email = email
        self.login_data = urllib.urlencode({'user[email]': email, 'user[password]': password})
        self.token = self.generateCredentials()
    #
    def generateCredentials(self):
        self.opener.open('https://auth.aiesec.org/users/sign_in', self.login_data)
        token = None
        for cookie in self.cj:
            if cookie.name == 'expa_token':
                token = cookie.value
        #
        if token is None:
            raise Exception('Unable to generate a token for {0}!'.format(self.email))
        #
        return token

    #gets mcs in expa
    def getMC(self,date):
        return None

    #get LCs
    def getLCs(self):
        r = requests.get('https://gis-api.aiesec.org/v2/committees/'+str(self.mc)+'.json?access_token='+self.token)
        d = json.loads(r.text)
        lcs_json = d['suboffices']
        lcs = []
        for lc in lcs_json:
            lcs.append(LC(lc['id'],lc['name']))
        #
        return lcs


    #gets opportunities
    def getOpportunities(self,start_date=datetime.datetime.now(),end_date=datetime.datetime.now()):

        payload = {'access_token': self.token,'filters[committee]':self.mc,
        'filters[last_interaction][from]':start_date.strftime('%y-%m-%d'),'filters[last_interaction][to]':end_date.strftime('%y-%m-%d')}
        r = requests.get('https://gis-api.aiesec.org/v2/opportunities.json',params=payload)

        d = json.loads(r.text)
        #print d
        ops = []
        for op in d['data']:
            #def __init__(self,expaid,title,url,programme,start_date,end_date,appsClosed,created,updated,status,lc,enabler): 
            ops.append(Opportunity(op['id'],op['title'],op['url'],
                op['programmes']['short_name'],op['earliest_start_date'],op['latest_end_date'],
                op['applications_close_date'],op['created_at'],op['updated_at'],op['status'],None,None))
        #
        return ops


    #def updates opportunities expecting an array
    def updateOpportunities(self,opportunitys):
        return None
    #get application 
    def getApplications(self,start_date=datetime.datetime.now(),end_date=datetime.datetime.now()):
        payload = {'access_token': self.token,'filters[committee]':self.mc,
        'filters[last_interaction][from]':start_date.strftime('%y-%m-%d'),'filters[last_interaction][to]':end_date.strftime('%y-%m-%d')}
        r = requests.get('https://gis-api.aiesec.org/v2/applications.json',params=payload)

        d = json.loads(r.text)
        apps = []
        for app in d['data']:
            #def __init__(self,expaid,url,status,currentStatus,personid,oppid):  
            apps.append(Application(app['id'],app['url'],app['status'],app['current_status'],app['person']['id'],app['opportunity']['id']))
        #
        return apps        
        
    #updates applicacionts expecting an array
    def updateApplications(seld,applications):
        return None
    #get enablers
    def getEnablers(self,start_date=datetime.datetime.now(),end_date=datetime.datetime.now()):
        payload = {'access_token': self.token,'filters[committee]':self.mc,
        'filters[last_interaction][from]':start_date.strftime('%y-%m-%d'),'filters[last_interaction][to]':end_date.strftime('%y-%m-%d')}
        r = requests.get('https://gis-api.aiesec.org/v2/organisations.json',params=payload)

        d = json.loads(r.text)
        ens = []
        for en in d['data']:
            print en
            #    def __init__(self,expaid,name,url,website,summary,gep,fromCop,tipo,size,status):    
            ens.append(Enabler(en['id'],en['name'],en['url'],en['website'],en['summary'],en['is_gep'],en['from_cop?'],
                en['organisation_type']['name'],en['organisation_size']['name'],en['status']))
        #
        return ens        
    #updates enablers expects array
    def updateEnabers(self,enablers):
        return None
    #gets people
    def getPeople(self,start_date=datetime.datetime.now(),end_date=datetime.datetime.now()):
        
        payload = {'access_token': self.token,'filters[home_committee]':self.mc,
        'filters[last_interaction][from]':start_date.strftime('%y-%m-%d'),'filters[last_interaction][to]':end_date.strftime('%y-%m-%d')}
        r = requests.get('https://gis-api.aiesec.org/v2/people.json',params=payload)

        d = json.loads(r.text)
        people = []
        for p in d['data']:
            print p
            #TODO: checar los programas
            #    def __init__(self,expaid,name,url,phone,email,contactedAt,createdAt,updatedAt,role,status,program): 
            people.append(People(p['id'],p['full_name'],p['url'],
                p['phone'],p['email'],p['contacted_at'],p['created_at'],p['updated_at'],None,p['status'],None))
        #
        return people
    #updates people expects array
    def updatePeople(seld,people):
        return None
#
#gis = GIS("enrique.suarez@aiesec.net","si no leo me aburro")
#gis.getPeople(datetime.datetime.now())


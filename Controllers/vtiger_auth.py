import hashlib
import logging
import requests
import json


class VTiger:


	def __init__(self):
		self.sessionId = ''
		self.userId = ''
		r = requests.get("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php?operation=getchallenge&username=admin")
		d = json.loads(r.text)
		self.challenge = d['result']['token']
		m = hashlib.md5()
		m.update(self.challenge+'wEB99P8LZP4Nac3')
		md5 = m.hexdigest()
		#print md5
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'login', 'username': 'admin', 'accessKey': md5})
		d = json.loads(r.text)
		self.sessionId = d['result']['sessionName']
		self.userId = d['result']['userId']
		print 'sesion de vitger iniciata'


	#logout
	def close(self):
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'logout', 'sessionName': self.sessionId})
		d = json.loads(r.text)
		return None
		

	#query
	#SELECT * | <column_list> | <count(*)>
	#
	#[WHERE <conditionals>]
	#[ORDER BY <column_list>]
	#[LIMIT [<m>, ] <n>]
	def query(self,query):
		url = 'http://knowledge.aiesec.org.mx/vtigercrm/webservice.php?operation=query&sessionName='+self.sessionId+'&query='+query
		#print url
		r = requests.get(url)
		d = json.loads(r.text)
		return d

	#create
	#operation=create
	#sessionName=sessionId        // Obtained through Login Operation
	#element=URLENCODED(JSONDATA) // JSONDATA - JSON Map of (fieldname=fieldvalue)
	#elementType=<TYPE>           // TYPE - Module Name
	def create(self,encodedData,elementType):
		print encodedData
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'create', 'sessionName': self.sessionId,
			'element':encodedData,'elementType':elementType})
		print r.text
		d = json.loads(r.text)
		print d

	#update
	#operation=update
	#sessionName=sessionId    // Obtained through Login Operation
	#element=URLENCODED(DATA) // DATA - Map of (fieldname=fieldvalue)
	def update(self,encodedData):
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'update', 'sessionName': self.sessionId,
			'element':encodedData})
		d = r.text
		print d

#	


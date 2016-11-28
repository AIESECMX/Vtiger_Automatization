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
	#login generates the sessionID and the userId
	def generateCredentials(self):
		m = hashlib.md5()
		m.update(self.challenge+'vBSOcWEq9WnKX9LU')
		md5 = m.hexdigest()
		print md5
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'login', 'username': 'admin', 'accessKey': md5})
		d = json.loads(r.text)
		self.sessionId = d['result']['sessionName']
		self.userId = d['result']['userId']


	#logout
	def close(self):
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'logout', 'sessionName': self.sessionId})
		d = json.loads(r.text)
		

	#query
	#SELECT * | <column_list> | <count(*)>
	#
	#[WHERE <conditionals>]
	#[ORDER BY <column_list>]
	#[LIMIT [<m>, ] <n>]
	def query(self,query):
		r = requests.get('http://knowledge.aiesec.org.mx/vtigercrm/webservice.php?operation=query&sessionName'+
			self.sessionId+'&query='+query)
		d = json.loads(r.text)
		print d

	#create
	#operation=create
	#sessionName=sessionId        // Obtained through Login Operation
	#element=URLENCODED(JSONDATA) // JSONDATA - JSON Map of (fieldname=fieldvalue)
	#elementType=<TYPE>           // TYPE - Module Name
	def create(self,encodedData,elementType):
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'create', 'sessionName': self.sessionId,
			'element':encodedData,'elementType':elementType})
		d = json.loads(r.text)

	#update
	#operation=update
	#sessionName=sessionId    // Obtained through Login Operation
	#element=URLENCODED(DATA) // DATA - Map of (fieldname=fieldvalue)
	def create(self,encodedData):
		r = requests.post("http://knowledge.aiesec.org.mx/vtigercrm/webservice.php",
			data={'operation': 'update', 'sessionName': self.sessionId,
			'element':encodedData})
		d = json.loads(r.text)

#	
vtiger = VTiger()
vtiger.generateCredentials()

vtiger.close()

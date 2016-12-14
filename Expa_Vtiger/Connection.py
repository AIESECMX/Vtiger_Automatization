import datetime
import sys
import urllib
import json
sys.path.insert(0,sys.path[0]+'/../Controllers')
from gis_auth import GIS
from vtiger_auth import VTiger

gis = GIS("enrique.suarez@aiesec.net","si no leo me aburro")
vtiger = VTiger()


# to put new LCs in the CRM dont call this every day but just when you explicitly want to make the udpate
def sync_LCs():
	lcs_query = 'select * from LC ;'
	vt_lcs = vtiger.query(lcs_query)
	vt_lcs = vt_lcs['result']
	print vt_lcs
	lcs = gis.getLCs()
	jump = False
	for lc in lcs:
		jump = False
		for lcv in vt_lcs:
			if str(lc.id) == lcv['lc_id']:
				#update
				print 'ya existe '+lc.name
				jump = True
				break
		#
		if jump:
			continue
		#create
		print 'create '+lc.name
		data ={'lc_id':lc.id,
					'name':lc.name					
					}
		#
		vtiger.create(json.dumps(data),'LC');


#
def sync_Enablers():
	lcs_query = 'select * from Enabler ;'
	vt_ens = vtiger.query(lcs_query)
	vt_ens = vt_ens['result']
	print vt_ens
	ens = gis.getEnablers()
	print ens
	jump = False
	for en in ens:
		jump = False
		print 'expa:'+str(en.id)
		for env in vt_ens:
			print 'vtiger:'+env['enabler_id']
			if str(en.id) == env['enabler_id']:
				#update
				print 'ya existe '+en.name
				if en.status != env['status']:
					env['status'] = en.status
					v = json.dumps(env)
					vtiger.update(v)
					print 'status update for :'+en.name
				jump = True
				break
		if jump:
			continue
			
		#create
		print 'create '+en.name
		data ={'enabler_id':en.id,
					'name':en.name,#name
					'url':en.url,#url
					'website':en.website,#website
					'summary':en.summary,#summary
					'ge':en.gep,#ge
					'from_cop':en.fromCop,#fromCop
					'type':en.tipo,#tipo
					'size':en.size,#size
					'status':en.status#status
					}
		#
		vtiger.create(json.dumps(data),'Enabler');
#
def sync_Opps():
	lcs_query = 'select * from Opportunity;'
	vt_opps = vtiger.query(lcs_query)
	vt_opps = vt_opps['result']
	#print vt_opps
	jump = False
	opps = gis.getOpportunities()
	for op in opps:
		jump = False
		for opv in vt_opps:
			if str(op.id) == opv['opportunity_id']:
				update = False
				#update
				enddate =op.end_date[:10] if op.end_date is not None else ''
				appsClosed = op.appsClosed[:10]  if op.appsClosed is not None else ''
				start_date = op.start_date[:10]  if op.start_date is not None else ''
				updated = op.updated[:10]  if op.updated is not None else ''
				opv['end_date'] = (enddate if enddate is not opv['end_date'] else opv['end_date'])
				opv['apps_closed'] = (appsClosed if appsClosed is not opv['apps_closed'] else opv['apps_closed'])
				opv['start_date'] = (start_date if start_date is not opv['start_date'] else opv['start_date'])
				opv['updated'] = (updated if updated is not opv['updated'] else opv['updated'])
				opv['status'] = op.status
				vtiger.update(json.dumps(opv))
				print 'update a : '+op.title
				jump = True
				break
		if jump:
			continue
		#create
		print 'create '+op.created
		data ={'opportunity_id':op.id,
					'end_date':op.end_date[:10] if op.end_date is not None else '',#end date
					'apps_closed':op.appsClosed[:10]  if op.appsClosed is not None else '',#app close
					'url':op.url,#url
					'start_date':op.start_date[:10]  if op.start_date is not None else '',#strts date
					'updated':op.updated[:10]  if op.updated is not None else '',#updated
					'status':op.status,#status
					'created':op.created[:10]  if op.created is not None else '',#created
					'title':op.title,#name
					'programme':op.programme
					}
		#
		vtiger.create(json.dumps(data),'Opportunity');
#
def sync_People():
	people_query = 'select * from People ;'
	vt_people = vtiger.query(people_query)
	vt_people = vt_people['result']
	print vt_people
	people = gis.getPeople()
	jump = False
	for person in people:
		jump = False
		for vt_person in vt_people:
			if str(person.id) == vt_person['people_id']:
				#update
				print 'update a '+person.name
				updated =person.updatedAt[:10] if person.updatedAt is not None else ''
				contacted = person.contactedAt[:10] if person.contactedAt is not None else ''
				vt_person['updated'] = (updated if updated is not vt_person['updated'] else vt_person['updated'])
				vt_person['contacted_at'] = (contacted if contacted is not vt_person['contacted_at'] else vt_person['contacted_at'])
				vt_person['phone'] = person.phone
				vtiger.update(json.dumps(vt_person))
				print 'update a '+person.name
				jump = True
				break
		if jump:
			continue
		#create
		print 'create '+person.name
		data ={'people_id':person.id,
					'updated':person.updatedAt[:10] if person.updatedAt is not None else '',#updated at
					'programme':person.program,#program
					'created':person.createdAt[:10] if person.createdAt is not None else '',#created at
					'contacted_at':person.contactedAt[:10] if person.contactedAt is not None else '',#contacted at
					'email':person.email,#mail
					'role':person.role,#role
					'phone':person.phone,#phone
					'name':person.name,#nonmbre
					'url':person.url#url
					}
		#
		vtiger.create(json.dumps(data),'People');


#s
def sync_Apps():
	apps_query = 'select * from Application ;'
	vt_apps = vtiger.query(apps_query)
	vt_apps = vt_apps['result']
	apps = gis.getApplications()
	jump = False
	for app in apps:
		jump = False
		for appv in vt_apps:
			if str(app.id) == appv['expa_id']:
				#update
				appv['current_status']=app.currentStatus
				appv['status']=app.status
				vtiger.update(json.dumps(appv))
				print 'update '+app.url
				jump = True
				break
		if jump:
			continue
			
		#create
		print 'create '+app.url
		data ={'expa_id':app.id,
					'url':app.url,#url
					'current_status':app.currentStatus,#current status
					'status':app.status#status
					}
		#
		vtiger.create(json.dumps(data),'Application');


#def
def update_test():
	apps_query = 'select * from Application ;'
	vt_apps = vtiger.query(apps_query)
	vt_apps = vt_apps['result'][0]
	v = json.dumps(vt_apps)
	print v



#()
sync_People()

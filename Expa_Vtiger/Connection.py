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
			if str(lc.id) == lcv['expa_id']:
				#update
				print 'ya existe '+lc.name
				jump = True
				break
		#
		if jump:
			continue
		#create
		print 'create '+lc.name
		data ={'expa_id':lc.id,
					'cf_806':lc.name,
					'cf_877':lc.name					
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
	jump = False
	for en in ens:
		jump = False
		print 'expa:'+str(en.id)
		for env in vt_ens:
			print 'vtiger:'+env['expa_id']
			if str(en.id) == env['expa_id']:
				#update
				print 'ya existe '+en.name
				if en.status != env['cf_824']:
					env['cf_824'] = en.status
					v = json.dumps(env)
					vtiger.update(v)
					print 'status update for :'+en.name
				jump = True
				break
		if jump:
			continue
			
		#create
		print 'create '+en.name
		data ={'expa_id':en.id,
					'cf_808':en.name,#name
					'cf_810':en.url,#url
					'cf_812':en.website,#website
					'cf_814':en.summary,#summary
					'cf_816':en.gep,#ge
					'cf_818':en.fromCop,#fromCop
					'cf_820':en.tipo,#tipo
					'cf_822':en.size,#size
					'cf_824':en.status#status
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
			if str(op.id) == opv['expa_id']:
				update = False
				#update
				enddate =op.end_date[:10] if op.end_date is not None else ''
				appsClosed = op.appsClosed[:10]  if op.appsClosed is not None else ''
				start_date = op.start_date[:10]  if op.start_date is not None else ''
				updated = op.updated[:10]  if op.updated is not None else ''
				opv['cf_774'] = (enddate if enddate is not opv['cf_774'] else opv['cf_774'])
				opv['cf_776'] = (appsClosed if appsClosed is not opv['cf_776'] else opv['cf_776'])
				opv['cf_772'] = (start_date if start_date is not opv['cf_772'] else opv['cf_772'])
				opv['cf_780'] = (updated if updated is not opv['cf_780'] else opv['cf_780'])
				opv['cf_782'] = op.status
				vtiger.update(json.dumps(opv))
				print 'update a : '+op.title
				jump = True
				break
		if jump:
			continue
		#create
		print 'create '+op.created
		data ={'expa_id':op.id,
					'cf_774':op.end_date[:10] if op.end_date is not None else '',#end date
					'cf_776':op.appsClosed[:10]  if op.appsClosed is not None else '',#app close
					'cf_770':op.url,#url
					'cf_772':op.start_date[:10]  if op.start_date is not None else '',#strts date
					'cf_780':op.updated[:10]  if op.updated is not None else '',#updated
					'cf_782':op.status,#status
					'cf_778':op.created[:10]  if op.created is not None else '',#created
					'cf_768':op.title,#name
					'cf_836':op.programme
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
			if str(person.id) == vt_person['expa_id']:
				#update
				print 'update a '+person.name
				updated =person.updatedAt[:10] if person.updatedAt is not None else ''
				contacted = person.contactedAt[:10] if person.contactedAt is not None else ''
				vt_person['cf_796'] = (updated if updated is not vt_person['cf_796'] else vt_person['cf_796'])
				vt_person['cf_794'] = (contacted if contacted is not vt_person['cf_794'] else vt_person['cf_794'])
				vt_person['cf_788'] = person.phone
				vt_person['cf_800'] = person.status
				vtiger.update(json.dumps(vt_person))
				print 'update a '+person.name
				jump = True
				break
		if jump:
			continue
		#create
		print 'create '+person.name
		data ={'expa_id':person.id,
					'cf_796':person.updatedAt[:10] if person.updatedAt is not None else '',#updated at
					'cf_802':person.program,#program
					'cf_794':person.createdAt[:10] if person.createdAt is not None else '',#created at
					'cf_792':person.contactedAt[:10] if person.contactedAt is not None else '',#contacted at
					'cf_790':person.email,#mail
					'cf_798':person.role,#role
					'cf_788':person.phone,#phone
					'cf_784':person.name,#nonmbre
					'cf_800':person.status,#status
					'cf_786':person.url#url
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
				appv['cf_843']=app.currentStatus
				appv['cf_841']=app.status
				vtiger.update(json.dumps(appv))
				print 'update '+app.url
				jump = True
				break
		if jump:
			continue
			
		#create
		print 'create '+app.url
		data ={'expa_id':app.id,
					'cf_839':app.url,#url
					'cf_843':app.currentStatus,#current status
					'cf_841':app.status,#status
					'cf_847':app.oppid,#opp
					'cf_845':app.personid#person
					}
		#
		vtiger.create(json.dumps(data),'Application');


#def
def update_test():
	apps_query = 'select * from Contacts ;'
	vt_apps = vtiger.query(apps_query)
	vt_apps = vt_apps['result'][0]
	v = json.dumps(vt_apps)
	print v



#()
sync_LCs()


from django.http import HttpResponse, HttpResponseRedirect
from random import randint
from django.template.loader import get_template
from django.shortcuts import render
from .forms import pat_reg_form,doc_reg_form,HospSearchForm, DocSearchForm, book_appt_form1, book_appt_form2
from .forms import hosp_reg_form, doc_hosp_form
from .models import Patients, Doctors, Hospitals, Appts
from hashlib import md5
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .views import get_slot
from django.http import JsonResponse

def doc_profile(request,doc_id):
	if request.user.username:
		login = True
	else:
		login = False
	username = request.user.username

	if not doc_id:
		return HttpResponseRedirect("/")
	else:
		#get doc specialities
		fname = Doctors.objects.get(id=doc_id).first_name
		lname = Doctors.objects.get(id=doc_id).last_name
		edu = Doctors.objects.get(id=doc_id).education
		alma_mater = Doctors.objects.get(id=doc_id).alma_mater

		if lname: 
			name = fname+' '+lname
		else:
			name = fname

		specialities = Doctors.objects.get(id=doc_id).specialities
		hospitals = Doctors.objects.get(id=doc_id).hospitals.values('hospital_name','city')

		return render(request,'doc_profile.html',{'utype':request.session['utype'],'uid': request.session['uid'], 'doc_name':name,'login_name': request.session['login_name'],'doc_id':doc_id,'specialities':specialities,'hospitals':hospitals,'edu':edu,'alma_mater':alma_mater})

def book_appt_res(request,pat_id,doc_id,slot_id,hosp_id,spec,dt):
	html = """
	patient id: {} <br>
	doctor_id: {} <br>
	slot_id: {} <br>
	hosp_id: {} <br>
	spec: {} <br>
	dt: {} <br>

	""".format(pat_id,doc_id,slot_id,hosp_id,spec,dt)

	return HttpResponse(html)	

@login_required(login_url='/login')
def doc_appt(request,doc_id):

	if not doc_id:
		return HttpResponseRedirect('/home')
		
	if request.session['utype'] == "doc":
		return HttpResponseRedirect("/")

	username = request.user.username

	if Patients.objects.filter(email=username).exists():
		utype = "pat"
		pat_id = Patients.objects.get(email=username).id 

	elif Doctors.objects.filter(email=username).exists():
		utype = "doc"

	doc = Doctors.objects.get(id=doc_id)
	spec = doc.specialities
	hospitals = doc.hospitals.values('id','hospital_name','city')

	if len(hospitals) == 0:
		return render(request, 'doc_appt.html')
	else:
		result = []

		for h in hospitals:
			hospital_name = h['hospital_name']
			hosp_id = h['id']
			hosp_city = h['city']
			today = date.today()
			hosp_data = []
			hosp_dict = {'hosp_name': hospital_name,'hosp_id':hosp_id,'hosp_city':hosp_city,'data': []}

			for k in range(1,11):
				dt = str(today + timedelta(k))

				for slot in range(1,5):
					if Appts.objects.filter(pat=pat_id,doc=doc_id,date=dt,slot=slot).exists():
						status = 'Booked by you'

					elif Appts.objects.filter(doc_id=doc_id,date=dt,slot=slot).count() < 4:
						status = 'Book now'
					else:
						status = 'Slot full'
					
					hosp_dict['data'].append({'dt':(today+timedelta(k)).strftime("%b %d %Y, %A"),'dt2':dt,'slot':get_slot(slot),'status':status})
					# hosp_dict['data'].append(k)
					
			result.append(hosp_dict)

		# return HttpResponse(result)
		return render(request,'doc_appt.html',{'user':request.user.username,'result':result,'doc_name':doc.first_name,'doc_id':doc_id,'pat_id':pat_id,'spec':spec,'slot_id':slot,})

@login_required(login_url='/login')
def view_pres(request,appt_id):
	login_id = request.session['uid'] 
	appt = Appts.objects.get(id=appt_id)
	doc_id = appt.doc_id

	if login_id == doc_id:
		return HttpResponseRedirect('/create_pres/{}'.format(appt_id))

	pat_id = appt.pat_id
	pat_name = Patients.objects.get(id=pat_id).first_name
	if Patients.objects.get(id=pat_id).last_name:
		pat_name = pat_name + ' ' + Patients.objects.get(id=pat_id).last_name

	doc_name = Doctors.objects.get(id=doc_id).first_name
	if Doctors.objects.get(id=doc_id).last_name:
		doc_name = doc_name + ' ' + Doctors.objects.get(id=doc_id).last_name

	# return HttpResponse("{} {} {} {}".format(request.session['utype'], request.session['uid'], appt.doc_id, appt_id))

	# return HttpResponse(appt_id)

	dt = appt.date 
	slot = get_slot(int(appt.slot))
	pres = appt.pres 
	refer = appt.refer 
	hosp_name = Hospitals.objects.get(id=appt.hosp_id).hospital_name
	department = appt.speciality


	if login_id != doc_id and login_id != pat_id:
		# return HttpResponseRedirect('/')
		return HttpResponse("Not authorised. {} {}".format(login_id, doc_id))

	if login_id == pat_id:
		data = {'dt':dt, 'slot':slot, 'pat_name': pat_name,'doc_name': doc_name, 'hosp_name': hosp_name, 'dept': department, 'pres': pres, 'refer': refer}
		return render(request, 'view_pres.html', data)
	

def reg_hosp(request):

	if request.method == 'POST':
		form = hosp_reg_form(request.POST)

		if form.is_valid():
			cd = form.cleaned_data

			hosp = form.save(commit=False)
			uid = randint(1000000,99999999)
			while Patients.objects.filter(uid=uid).exists() or Doctors.objects.filter(uid=uid).exists() or Hospitals.objects.filter(uid=uid).exists():
				uid = randint(1000000,99999999)

			hosp.uid = uid
			hosp.save()

			return render(request,"reg_hosp.html",{'cd':'Hospital Registration Complete.'})

	else:
		form = hosp_reg_form({'specialities': 'Cardiology, Gastroenterology, Opthalmology, Psychiatry, Neurology, Orthpaedia'})
		# form = hosp_reg_form()
		

	return render(request,"reg_hosp.html",{'form':form})

def signup(request):
	form = pat_reg_form()

	return render(request, 'ajax.html', {'form':form})

def validate_username(request):
    username = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def add_hd(request):
	hosp_id = request.GET.get('hosp_id', None)
	doc_id = request.GET.get('doc_id', None)

	status = "unknown error"

	if Hospitals.objects.filter(id=hosp_id,doctors=doc_id).exists():
		status_msg = "Hospital id {} and Doctor id {} are already linked".format(hosp_id,doc_id)
		status_code = 0
	else:
		Hospitals.objects.get(id=hosp_id).doctors.add(doc_id)
		status_msg = "Hospital id {} and Doctor id {} are successfully linked".format(hosp_id,doc_id)
		status_code = 1

	data = {
		# 'result': "Received hosp_id {} doc_id {}".format(hosp_id, doc_id)
		'status_msg': status_msg, 'status_code': status_code
	}

	return JsonResponse(data)

def remove_hd(request):
	hosp_id = request.GET.get('hosp_id', None)
	doc_id = request.GET.get('doc_id', None)

	Hospitals.objects.get(id=hosp_id).doctors.remove(doc_id)

	data = {
		'status': "Link between hosp_id {} doc_id {} removed".format(hosp_id, doc_id)
	}

	return JsonResponse(data)

def doc_name(id):
	if Doctors.objects.get(id=id).last_name:
		return Doctors.objects.get(id=id).first_name + " " + Doctors.objects.get(id=id).last_name
	else:
		return Doctors.objects.get(id=id).first_name

@login_required(login_url='/login')
def doc_hosp(request):
	form = doc_hosp_form(request.POST or None)
	cd = ''
	if request.method == 'POST':
		if form.is_valid():
			cd = form.cleaned_data

	hospitals = Hospitals.objects.all()

	hosp_list = []

	for hosp in hospitals:
		doctors = hosp.doctors.values('id','specialities')
		doc_list = []
		for d in doctors:
			name = doc_name(d['id'])
			doc = """
			<a href='doc_profile/{}'>{}</a> ({})
			""".format(d['id'],name, d['specialities'])

			# doc_list.append(doc)
			# docs = ','.join(doc_list)
			doc_list.append({'name':name, 'id': d['id'], 'spec': d['specialities']})
		
		hosp_list.append({'hospital_name': hosp.hospital_name, 'hosp_id': hosp.id, 'doctors': doc_list})

	return render(request,'doc_hosp.html',{'form':form, 'data': hosp_list, 'cd': cd})

@login_required(login_url="/login")
def cancel_appt(request):
	appt_id = request.GET.get('appt_id',None)
	Appts.objects.get(id=appt_id).delete()

	data = {'status': "Appointment id {} deleted successfully".format(appt_id)}

	return JsonResponse(data)

@login_required(login_url="/login")
def check_doc_hosp_avail(request):
	hosp_id = request.GET.get('hosp_id',None)
	spec = request.GET.get('spec',None)

	num_docs = Hospitals.objects.get(id=hosp_id).doctors.filter(specialities__icontains=spec).count()

	data = {
		'num_docs': num_docs
	}

	return JsonResponse(data)
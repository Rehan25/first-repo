from django.http import HttpResponse, HttpResponseRedirect
from random import randint
from django.template.loader import get_template
from django.shortcuts import render
from .forms import pat_reg_form,doc_reg_form,HospSearchForm, DocSearchForm, book_appt_form1, book_appt_form2, create_pres_form
from .models import AuthUser,Patients, Doctors, Hospitals, Appts
from hashlib import md5
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django import forms

#def hello(request):
#   return HttpResponse("Hello world") 

def get_slot(n):
	d = {1:'11 AM - 12 PM',2:'12 PM - 1 PM',3:'2 PM - 3 PM',4:'3 PM - 4 PM'}
	return d[n]

def index(request):
	# t = get_template('base.html')
	# html = t.render({'user':'to PMS portal'})
	# return HttpResponse(html)
	if request.user.is_authenticated:
		return HttpResponseRedirect('/home')

	return render(request,'main.html')

def login(request):
	status = ''

	if request.method == 'POST':
		# if form.is_valid():
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request,username=username,password=password)

		if user is not None:
			auth_login(request,user)
			status = 'logged in'
			if Patients.objects.filter(email=username).exists():
				utype = 'pat'
				uid = Patients.objects.get(email=username).id
				login_name = Patients.objects.get(email=username).first_name
			elif Doctors.objects.filter(email=username).exists():
				utype = 'doc'
				uid = Doctors.objects.get(email=username).id
				login_name = Doctors.objects.get(email=username).first_name

			request.session['utype'] = utype
			request.session['uid'] = uid
			request.session['login_name'] = login_name
			request.session.set_expiry(request.session.get_expiry_age())

			if request.GET.get('next'):
				return HttpResponseRedirect(request.GET.get('next'))
			else:
				return HttpResponseRedirect('/home')
		else:
			status = 'Invalid credentials'
		
	return render(request,'login.html',{'status': status})

def logout(request):
	if request.user.is_authenticated:
		auth_logout(request)
		return HttpResponseRedirect('/')
	else:
		return HttpResponse("Not logged in")

def register(request,utype=None):
	if not utype:
		return render(request,'reg_home.html')
	else:
		cd = ''
		submitted = False
		newuser = ''
		if request.method == 'POST':

			if utype == 'p':
				form = pat_reg_form(request.POST)
				ut = 1
			elif utype == 'd':
				form = doc_reg_form(request.POST)
				ut = 2

			if form.is_valid():
				# cd = 'qqq'
				cd = form.cleaned_data

				newuser = form.save(commit=False)
				# newuser.specialities = ','.join(newuser.specialities)
				#Create unique user id
				uid = randint(1000000,99999999)
				while Patients.objects.filter(uid=uid).exists() or Doctors.objects.filter(uid=uid).exists() or Hospitals.objects.filter(uid=uid).exists():
					uid = randint(1000000,99999999)

				newuser.uid = uid
				user = User.objects.filter(username=newuser.email)

				if user.exists():
				    raise forms.ValidationError("User with that email id is already registered.")

				user = User.objects.create_user(newuser.email,newuser.email,newuser.password)
				newuser.password = md5(newuser.password.encode('utf-8')).hexdigest()
				newuser.save()

				if Doctors.objects.filter(uid=uid).exists():
					doc_id = Doctors.objects.get(uid=uid).id
					hosp_id = int(cd['hospitals'])

					hosp = Hospitals.objects.get(id=hosp_id) 
					hosp.doctors.add(doc_id)

				submitted = True
				
				# return HttpResponseRedirect('/contact?submitted=True')
				return render(request,'register.html',{'form':form,'submitted': submitted,'utype':utype})
		else:
			if utype == 'p':
				form = pat_reg_form()
			elif utype == 'd':
				form = doc_reg_form()

			# if 'submitted' in request.GET:
			# 	submitted = True
			return render(request,'register.html',{'form':form,'submitted': submitted,'utype':utype,'cd':cd})

		return render(request,'register.html',{'form':form,'submitted': submitted,'utype':utype,'cd':cd})

		html = """
		<p><label>Specialities:</label> <ul id="id_specialities">\n    <li><label for="id_specialities_0"><input type="checkbox" name="specialities" value="a" id="id_specialities_0">\n A</label>\n\n</li>\n    <li><label for="id_specialities_1"><input type="checkbox" name="specialities" value="b" id="id_specialities_1">\n b</label>\n\n</li>\n    <li><label for="id_specialities_2"><input type="checkbox" name="specialities" value="c" id="id_specialities_2">\n c</label>\n\n</li>\n</ul></p>
		"""
		# return HttpResponse(html)

@login_required(login_url='/login')
def home(request):
	username = request.user.username
	utype = request.session['utype']

	date_joined = AuthUser.objects.get(username="{}".format(username)).date_joined.strftime("%A, %b %d %Y")
	last_login = AuthUser.objects.get(username=username).last_login.strftime("%A, %b %d %Y")

	if Patients.objects.filter(email=username).exists():
	
		first_name = Patients.objects.filter(email=username)[0].first_name
		pat_id = Patients.objects.get(email=username).id

		appts = Appts.objects.filter(pat_id=pat_id).order_by('date')

		if len(appts) != 0:

			result_past, result_today, result_future = [],[],[]
			today = date.today()

			for x in appts:
				appt_id = x.id
				spec = x.speciality
				doctor_name = Doctors.objects.get(id=x.doc_id).first_name
				hospital_name = Hospitals.objects.get(id=x.hosp_id).hospital_name
				slot_name = get_slot(int(x.slot))
				dt = (x.date).strftime("%b %d %Y, %A")

				if x.pres == None and x.refer == None:
					pres_status = 0
				else:
					pres_status = 1

				if x.date < today:
					result_past.append({'hospital_name':hospital_name,'doc_id':x.doc_id,'doctor_name': doctor_name,'spec':spec,'dt':dt,'slot':slot_name,'appt_id':appt_id, 'pres_status': pres_status})
				elif x.date == today:
					result_today.append({'hospital_name':hospital_name,'doc_id':x.doc_id,'doctor_name': doctor_name,'spec':spec,'dt':dt,'slot':slot_name, 'appt_id': appt_id, 'pres_status': pres_status})
				elif x.date > today:
					result_future.append({'hospital_name':hospital_name,'doc_id':x.doc_id,'doctor_name': doctor_name,'spec':spec,'dt':dt,'slot':slot_name, 'appt_id': appt_id, 'pres_status': pres_status})


			return render(request,'home.html',{'date_joined': date_joined,'last_login': last_login,'utype':utype,'result_past': result_past,'result_today':result_today,'result_future': result_future,'first_name': first_name})
		else:
			return render(request,'home.html',{'date_joined': date_joined,'last_login': last_login})

	elif Doctors.objects.filter(email=username).exists():
		first_name = Doctors.objects.filter(email=username)[0].first_name
		doc_id = Doctors.objects.get(email=username).id

		appts = Appts.objects.filter(doc_id=doc_id).order_by('date')
		today = date.today()

		if len(appts) != 0:

			result_past, result_today, result_future = [],[],[]

			for x in appts:
				appt_id = x.id
				spec = x.speciality
				pat_name = Patients.objects.get(id=x.pat_id).first_name
				hospital_name = Hospitals.objects.get(id=x.hosp_id).hospital_name
				slot_name = get_slot(int(x.slot))
				dt = (x.date).strftime("%b %d %Y, %A")

				if x.pres:
					status = 1
				else: 
					status = 0

				if x.date < today:
					result_past.append({'appt_id': appt_id,'hospital_name':hospital_name,'doc_id':x.doc_id,'pat_name': pat_name,'spec':spec,'dt':dt,'slot':slot_name, 'status': status})
				elif x.date == today:
					result_today.append({'appt_id': appt_id,'hospital_name':hospital_name,'doc_id':x.doc_id,'pat_name': pat_name,'spec':spec,'dt':dt,'slot':slot_name, 'status': status})
				elif x.date > today:
					result_future.append({'appt_id': appt_id,'hospital_name':hospital_name,'doc_id':x.doc_id,'pat_name': pat_name,'spec':spec,'dt':dt,'slot':slot_name, 'status': status})
			
			return render(request,'home-doc.html',{'date_joined': date_joined,'last_login': last_login,'first_name': first_name,'doc_id': doc_id,'result_past': result_past, 'result_today': result_today,'result_future':result_future, 'first_name': first_name})
		else:
			return render(request,'home-doc.html',{'date_joined': date_joined,'last_login': last_login})

@login_required(login_url='/login')
def search(request,utype=None):
	if not utype:
		return render(request,'search_home.html')

	else:

		username = request.user.username
		if request.session['utype'] == "pat":
			first_name = Patients.objects.filter(email=username)[0].first_name
		elif request.session['utype'] == "doc":
			first_name = Doctors.objects.filter(email=username)[0].first_name

		if request.method == 'POST':
			if utype == 'h':
				form = HospSearchForm(request.POST)
				cd = ''
				hosp_list = ''

				if form.is_valid():
					cd = form.cleaned_data
					city = cd['city']
					area = cd['area']
					spec = cd['specialities']

					if city == 'all': city = ''
					if area == 'all': area = ''
					if spec == 'all': spec = ''

				hosp_list = list(Hospitals.objects.filter(city__icontains=city,area__icontains=area, specialities__icontains=spec).values('id','hospital_name','city','area','specialities'))

				i = 0
				for h in hosp_list:
					hosp_list[i].update({'doctors': list(Hospitals.objects.get(id=h['id']).doctors.values('id','first_name','last_name','specialities'))})
					i += 1

				return render(request,'search.html',{'form':form,'hosp_list': hosp_list, 'first_name': first_name})

			elif utype == 'd':
				
				form = DocSearchForm(request.POST)
				if form.is_valid():
					cd = form.cleaned_data
					spec = cd['specialities']
					city = cd['cities']

				doc_list = []
				if spec == 'all': spec = ''
				if city == 'all': city = ''

				q1 = Doctors.objects.filter(specialities__icontains=spec)

				for d in q1:
					doc_id = d.id 
					spec = d.specialities

					if d.last_name:
						doc_name = d.first_name + " " + d.last_name
					else:
						doc_name = d.first_name

					hospitals = d.hospitals.filter(city__icontains=city).values('hospital_name','city')

					if len(hospitals) != 0:

						hlist = []
						for h in hospitals:
							hosp_name = h['hospital_name']
							hosp_city = h['city']
							hlist.append({'hosp_name': hosp_name, 'hosp_city': hosp_city})

						doc_list.append({'doc_name': doc_name,'doc_id': doc_id, 'spec': spec,'hospitals': hlist })

				
				return render(request,'search_doc.html',{'form':form,'doc_list':doc_list})

		else:
			if utype == 'h':
				form = HospSearchForm()
				return render(request,'search.html',{'form':form})

			elif utype == 'd':
				cd = 'x'
				form = DocSearchForm()
				return render(request,'search_doc.html',{'form':form,'cd':cd})

@login_required(login_url='/login')
def book_appt(request,pat_id,doc_id,slot_id,hosp_id,spec,dt):
	if not slot_id:
		cd = ''
		form = book_appt_form1(request.POST or None)

		doc_avail = ''

		if request.method == 'POST':
			if form.is_valid():
				cd = form.cleaned_data


				hosp_id = cd['hospitals']
				spec = cd['specialities']
				
				pat_id = Patients.objects.get(email=request.user.username).id
				hosp_name = Hospitals.objects.get(id=hosp_id).hospital_name

				doctors = list(Hospitals.objects.get(id=hosp_id).doctors.filter(specialities__icontains=spec).values('id','first_name','last_name'))
				doc_avail = len(doctors)

				today = date.today()

				dt_list = []

				for k in range(1,11):
					dt = str(today + timedelta(k))
					i = 0
					
					status = ''
					for d in doctors:
						doc_id = d['id']

						slot_data = []

						for slot in range(1,5):
							if Appts.objects.filter(pat=pat_id,doc=doc_id,date=dt,slot=slot).exists():
								status = 'Booked by you'

							elif Appts.objects.filter(doc_id=doc_id,date=dt,slot=slot).count() < 4:
								# x[i].update({'date':dt})
								status = 'Book now'
							
							else:
								status = 'This slot is full'

							slot_data.append({'slot_id': slot, 'slot': get_slot(slot),'status': status})

						dt_list.append({'dt':(today + timedelta(k)).strftime("%b %d %Y, %A"),'dt2':dt,'doctor':d,'slot_data': slot_data})
				

				return render(request,'appt_home.html',{'result': dt_list,'pat_id': pat_id,'hosp_id':hosp_id,'hosp_name':hosp_name,'spec':spec, 'doc_avail': doc_avail})

		return render(request,'appt_home.html',{'form': form,'cd':cd})

	else:
		if request.session['utype'] == "doc":
			return HttpResponse("Doctors cannot create appointments as of now")

		pat_fname = Patients.objects.get(id=pat_id).first_name
		doc_name = Doctors.objects.get(id=doc_id).first_name
		hospital_name = Hospitals.objects.get(id=hosp_id).hospital_name
		slot_name = get_slot(int(slot_id))
		hospital_city = Hospitals.objects.get(id=hosp_id).city

		Appts(pat=Patients.objects.get(id=pat_id),doc=Doctors.objects.get(id=doc_id),hosp=Hospitals.objects.get(id=hosp_id),slot=slot_id,speciality=spec,date=dt).save()
		
		appt_id = Appts.objects.get(pat=Patients.objects.get(id=pat_id),doc=Doctors.objects.get(id=doc_id),hosp=Hospitals.objects.get(id=hosp_id),slot=slot_id,date=dt,speciality=spec).id

		return render(request,'appt_home.html',{'pat_fname':pat_fname,'doc_name':doc_name,'hospital_name':hospital_name,'hospital_city':hospital_city,'slot_name':slot_name,'spec':spec,'dt':dt,'appt_id':appt_id})

		html = """
		patient id: {} <br>
		doctor_id: {} <br>
		slot_id: {} <br>
		slot_name: {} <br>
		hosp_id: {} <br>
		spec: {} <br>
		dt: {} <br>

		""".format(pat_id,doc_id,slot_id,slot_name,hosp_id,spec,dt)

		# return HttpResponse(html)

@login_required(login_url='/login')
def create_pres(request,appt_id):

	if request.session['utype'] != 'doc':
		return HttpResponseRedirect('/')

	# form = create_pres_form(request.POST or None)

	if request.method == 'POST':
		form = create_pres_form(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			Appts.objects.filter(id=appt_id).update(pres=cd['pres'],refer=cd['refer'])

			return render(request,'create_pres.html',{'cd':cd,'appt_id':appt_id})

	else:
		appt = Appts.objects.get(id=appt_id)
		doc_id = appt.doc_id
		if request.session['uid'] != doc_id:
			return HttpResponseRedirect("/")

		pres = appt.pres
		refer = appt.refer 
		pat_name = Patients.objects.get(id=appt.pat_id).first_name
		hospital_name = Hospitals.objects.get(id=appt.hosp_id).hospital_name
		username = request.user.username
		doc_name = Doctors.objects.get(email=username).first_name

		form = create_pres_form({'pres':pres,'refer':refer})

		data = {'form':form,'pres':pres,'refer': refer, 'doc_id':doc_id,'doc_name':doc_name,'pat_name': pat_name,'hospital_name': hospital_name,'spec':appt.speciality,'slot':get_slot(int(appt.slot)),'dt':appt.date}

		return render(request,'create_pres.html',data)
		# return HttpResponse(request.session['utype'])
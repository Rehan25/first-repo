from django import forms
from django.forms import ModelForm
from django.db.models.fields import BLANK_CHOICE_DASH
from .models import Patients, Doctors, Hospitals, Appts

def doc_name(id):
	if Doctors.objects.get(id=id).last_name:
		return Doctors.objects.get(id=id).first_name + " " + Doctors.objects.get(id=id).last_name
	else:
		return Doctors.objects.get(id=id).first_name

class doc_hosp_form(forms.Form):
	hospitals = forms.ChoiceField(choices=[(choice.pk, choice) for choice in Hospitals.objects.all()], widget=forms.Select(attrs={'class':'form-control'}))
	doctors = forms.ChoiceField(choices=[(choice.pk, doc_name(choice.pk)) for choice in Doctors.objects.all()], widget=forms.Select(attrs={'class':'form-control'}))

class hosp_reg_form(ModelForm):
	class Meta:
		model = Hospitals
		fields = ['hospital_name','area','city','specialities']

		widgets = {
		'hospital_name': forms.TextInput(attrs={'class' : 'form-control'}),
		'specialities': forms.TextInput(attrs={'class' : 'form-control'}),
		'area': forms.TextInput(attrs={'class' : 'form-control'}),
		'city': forms.TextInput(attrs={'class' : 'form-control'}),
		}

		help_texts = {
		'area': ('Locality name within city')
		}

class create_pres_form(ModelForm):
	class Meta:
		model = Appts
		fields = ['pres','refer']

		widgets = {
		'pres': forms.Textarea(attrs={'class' : 'form-control','style':'height: 300px'}),
		'refer': forms.Textarea(attrs={'class' : 'form-control','style':'height: 100px'})
		}

		help_texts = {
		'refer': ('Refer to another doctor, lab or hospital'),
		}

class book_appt_form1(forms.Form):
	# hospitals = forms.ModelChoiceField(queryset=Hospitals.objects.all().values('id','hospital_name'), widget=forms.Select(attrs={'class':'form-control',"onChange":'refresh()'}))
	hospitals = forms.ChoiceField(choices=[(choice.pk, choice) for choice in Hospitals.objects.all()], widget=forms.Select(attrs={'class':'form-control'}))
	sp_choices = (
			    ('Cardiology', 'Cardiology'),
			    ('Neurology', 'Neurology'),
			    ('Gastroenterology', 'Gastroenterology'),
			    ('General Medicine', 'General Medicine'),
			    ('Psychiatry', 'Psychiatry'),
			    ('Orthopaedia', 'Orthopaedia'),
			    ('Opthalmology', 'Opthalmology'),
			   )
	specialities = forms.ChoiceField(choices=sp_choices, widget=forms.Select(attrs={'class':'form-control'}))

class book_appt_form2(forms.Form):
	def __init__(self,request,*args,**kwargs):
		# self.hosp_id = kwargs.pop('hosp_id')
		super(book_appt_form2,self).__init__(*args,**kwargs)
		
		# hosp_id = request.session['hosp_id']
		# if hosp_id:
		# 	sp_list = list(Hospitals.objects.filter(id=hosp_id).values('specialities')[0].values())[0].split(',')

		# 	sp_choices = []

		# 	for x in sp_list:
		# 		sp_choices.append((x,x))

		# 	sp_choices = tuple(sp_choices)

		sp_choices = (
					('all','All'),
				    ('Cardiology', 'Cardiology'),
				    ('Neurology', 'Neurology'),
				    ('Gastroenterology', 'Gastroenterology'),
				    ('General Medicine', 'General Medicine'),
				    ('Psychiatry', 'Psychiatry'),
				    ('Orthopaedia', 'Orthopaedia'),
				    ('Opthalmology', 'Opthalmology'),
				   )

		self.fields['specialities'].widget = forms.Select(choices=sp_choices,attrs={'class':'form-control',"onChange":'refresh()'})

	specialities = forms.ChoiceField()
	# sp_choices = []

	# for x in sp_list:
	# 	sp_choices.append((x,x))

	# sp_choices = tuple(sp_choices)
	# specialities = forms.ChoiceField(choices=sp_choices, widget=forms.Select(attrs={'class':'form-control',"onChange":'refresh()'}))


class HospSearchForm(ModelForm):
	class Meta:
		model = Hospitals
		fields = ['area','specialities','city']

		areas = list(Hospitals.objects.values_list('area',flat=True))
		area_choices = [('all','All')]
		n = 1 

		for a in areas:
			area_choices.append((a,a))
			n += 1
		# area_choices.append(('all','All'))
		area_choices = tuple(area_choices)

		cities = list(Hospitals.objects.values_list('city',flat=True).distinct())
		city_choices = [('all','All')]
		n = 1

		for x in cities:
			city_choices.append((x,x))
			n += 1

		city_choices = tuple(city_choices)

		# specialities = []
		# sps = Hospitals.objects.values_list('specialities',flat=True)

		# for sp in sps:
		# 	specialities = specialities + sp.split(',')

		# specialities SELECT * FROM= list(set(specialities))

		# spec_choices = [('all','All')]
		# n = 1
		# for s in specialities:
		# 	spec_choices.append((s,s))
		# 	n += 1

		# spec_choices = tuple(spec_choices)
		spec_choices = (
					('all','All'),
				    ('Cardiology', 'Cardiology'),
				    ('Neurology', 'Neurology'),
				    ('Gastroenterology', 'Gastroenterology'),
				    ('General Medicine', 'General Medicine'),
				    ('Psychiatry', 'Psychiatry'),
				    ('Orthopaedia', 'Orthopaedia'),
				    ('Opthalmology', 'Opthalmology'),
				   )


		widgets = {
		'city': forms.Select(choices=city_choices,attrs={'class': 'form-control'}),
		'area': forms.Select(choices=area_choices,attrs={'class': 'form-control'}),
		'specialities': forms.Select(choices=spec_choices,attrs={'class': 'form-control'})
		}

class DocSearchForm(forms.Form):
	# specialities = []
	# sps = Hospitals.objects.values_list('specialities',flat=True)

	# for sp in sps:
	# 	specialities = specialities + sp.split(',')

	# specialities = list(set(specialities))

	# spec_choices = [('all','All')]
	# n = 1
	# for s in specialities:
	# 	spec_choices.append((s,s))
	# 	n += 1

	# spec_choices = tuple(spec_choices)

	spec_choices = (
					('all','All'),
				    ('Cardiology', 'Cardiology'),
				    ('Neurology', 'Neurology'),
				    ('Gastroenterology', 'Gastroenterology'),
				    ('General Medicine', 'General Medicine'),
				    ('Psychiatry', 'Psychiatry'),
				    ('Orthopaedia', 'Orthopaedia'),
				    ('Opthalmology', 'Opthalmology'),
				   )

	specialities = forms.ChoiceField(choices = spec_choices,widget=forms.Select(attrs={'class':'form-control'}), required=True)
	# widgets = {
	# 'specialities': forms.Select(choices=spec_choices,attrs={'class':'form-control'})
	# }
	cities = forms.ChoiceField(choices = [('all','All')]+ [(x['city'],x['city']) for x in Hospitals.objects.values('city').distinct()], widget = forms.Select(attrs={'class':'form-control'}))

class doc_reg_form(ModelForm):
	hospitals = forms.ChoiceField(choices=[(choice.pk, choice) for choice in Hospitals.objects.all()], widget=forms.Select(attrs={'class':'form-control'}))
	class Meta:
		model = Doctors
		fields = ['first_name','last_name','email','gender','specialities','password','mobile','education','alma_mater','total_exp']

		gender_choices = (('1', 'Male'),('2', 'Female'),('3','Third gender'))

		EVENT_FORM_CHOICES = ((1, (u'aaaa')),(2, (u'bbbb')),(3, (u'cccc')),(4, (u'dddd')),(5, (u'eeee')))

		spec_choices = (
					    ('Cardiology', 'Cardiology'),
					    ('Neurology', 'Neurology'),
					    ('Gastroenterology', 'Gastroenterology'),
					    ('General Medicine', 'General Medicine'),
					    ('Psychiatry', 'Psychiatry'),
					    ('Orthopaedia', 'Orthopaedia'),
					    ('Opthalmology', 'Opthalmology'),
					   )

		widgets = {
		# 'hospitals': forms.Select(attrs={'class':'form-control'}),
		'education': forms.TextInput(attrs={'class' : 'form-control'}),
		'first_name': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter First Name'}),
		'last_name': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter Last Name'}),
		'email': forms.EmailInput(attrs={'class' : 'form-control','placeholder' : 'Enter email ID'}),
		'gender': forms.Select(choices=BLANK_CHOICE_DASH+list(gender_choices),attrs={'class' : 'form-control'}),
		'password': forms.PasswordInput(attrs={'class' : 'form-control'}),
		'mobile': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter mobile number'}),
		'specialities': forms.Select(choices=BLANK_CHOICE_DASH + list(spec_choices),attrs={'class' : 'form-control'}),
		'alma_mater': forms.TextInput(attrs={'class' : 'form-control','placeholder' : ''}),
		'total_exp': forms.TextInput(attrs={'class' : 'form-control','placeholder' : ''})
		}

		help_texts = {
		'email': ('This will be your login ID'),
		'education': ('Mention your degrees comma separated'),
		'total_exp': ('In no. of years')
		}


class pat_reg_form(ModelForm):
	class Meta:
		model = Patients
		fields = ['first_name','last_name','email','gender','password','mobile','address','city','pincode']

		gender_choices = (('1', 'Male'),('2', 'Female'),('3','Third gender'))

		# gender_choices =  (
		# 				    ('Select One',
		# 				    (('North South University', 'North South University'),
		# 				    ('BRAC University', 'BRAC University'),)),
		# 				)	

		widgets = {
		'first_name': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter First Name'}),
		'last_name': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter Last Name'}),
		'gender': forms.Select(choices=BLANK_CHOICE_DASH + list(gender_choices),attrs={'class' : 'form-control'}),
		'email': forms.EmailInput(attrs={'class' : 'form-control','placeholder' : 'Enter email ID'}),
		'password': forms.PasswordInput(attrs={'class' : 'form-control'}),
		'mobile': forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter mobile number'}),
		'address': forms.Textarea(attrs={'class' : 'form-control','style' : 'height: 100px'}),
		'city': forms.TextInput(attrs={'class' : 'form-control','placeholder' : ''}),
		'pincode': forms.TextInput(attrs={'class' : 'form-control','placeholder' : ''})

		}

		help_texts = {
		'email': ('This will be your login ID'),
		}

class reg_form(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter First Name'}))
	last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter Last Name'}))
	dob = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control'}))
	gender = forms.CharField(widget=forms.Select(choices=(('1','Male'),('2','Female'),('3','Third gender')),attrs={'class' : 'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control','placeholder' : 'Enter email ID'}),help_text='This will be your login ID')
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
	mobile = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Enter mobile number'}))
	address = forms.CharField(required=False,widget=forms.Textarea(attrs={'class' : 'form-control','placeholder' : ''}))
	city = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control','placeholder' : ''}))
	pincode = forms.CharField(required=False,widget=forms.TextInput(attrs={'class' : 'form-control','placeholder' : ''}))
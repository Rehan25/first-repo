from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm, DjangoForm

def contact(request):

	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():

			cd = form.cleaned_data
			return HttpResponseRedirect('')

			# name = form.cleaned_data['name']
			# email = form.cleaned_data['email']
			# category = form.cleaned_data['category']
			# subject = form.cleaned_data['subject']
			# body = form.cleaned_data['body']
	else:

		form = ContactForm()
		return render(request,'form.html',{'form':form })

def django_detail(request):

	if request.method == 'POST':
		form = DjangoForm(request.POST)
		if form.is_valid():

			form.save()
			return HttpResponseRedirect('/django/')
	else:
		form = DjangoForm()
		return render(request,'form.html',{'form': form })
# Create your views here.

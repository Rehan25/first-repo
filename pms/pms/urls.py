"""pms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url

from pms.views import index, login, register, logout, home, search, book_appt, create_pres
from pms.views2 import doc_profile, book_appt_res, doc_appt, view_pres, reg_hosp, signup, validate_username, doc_hosp, add_hd, remove_hd
from pms.views2 import cancel_appt, check_doc_hosp_avail

urlpatterns = [
	path('admin/', admin.site.urls),
	path('register/', register),
	path('',index),
	# path(r'login/(.)',login),
    url(r'login/',login),
    #ajax urls
    url(r'signup/',signup), url(r'validate_username',validate_username), url(r'add_hd',add_hd), url(r'remove_hd',remove_hd),
    url(r'cancel_appt', cancel_appt), url(r'check_doc_hosp_avail', check_doc_hosp_avail),
    url(r'reg_hosp/',reg_hosp),
    url(r'logout/',logout),
	url(r'^register/(?:(?P<utype>.)/)?$',register),
    url(r'home/',home),
    url(r'search/(?:(?P<utype>.)/)?$',search),
    url(r'doc_profile/(?:(?P<doc_id>[0-9]+)/)?$',doc_profile),
    # url(r'book_appt/(?:(?P<hosp_id>[0-9]+)/(?P<spec>[a-zA-Z]+))/?$',book_appt))
    # url(r'book_appt/?(?P<hosp_id>[0-9]+)?/?(?P<spec>[a-zA-Z]+)?/$',book_appt),)
    # url(r'book_appt/',book_appt),
    url(r'book_appt/?(?P<pat_id>[0-9]+)?/?(?P<doc_id>[0-9]+)?/?(?P<slot_id>[0-9]+)?/?(?P<hosp_id>[0-9]+)?/?(?P<spec>[ a-zA-Z]+)?/?(?P<dt>[0-9-]+)?/$',book_appt),
    url(r'create_pres/(?:(?P<appt_id>[0-9]+)/)?$',create_pres),
    url(r'view_pres/(?:(?P<appt_id>[0-9]+)/)?$',view_pres),
    url(r'doc_appt/(?:(?P<doc_id>[0-9]+)/)?$',doc_appt),
    url(r'doc_hosp/',doc_hosp)
]


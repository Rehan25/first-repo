from django.urls import path
from .import views

urlpatterns = [
   path('', views.contact,name='contact'),
   path('django',views.django_detail,name='django_detail'),
]
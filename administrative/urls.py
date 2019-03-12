from django.conf.urls import url
from administrative import views

# TEMPLATE TAGGING
app_name = 'administrative'

urlpatterns = [
	url(r'^administrative/$', views.admin_home, name='admin_home'),
	url(r'^accountM/$', views.acc_management, name='acc_management'),
	url(r'^unitsM/$', views.unit_management, name='unit_management'),
	url(r'^teachingspace/$', views.space_management, name='space_management'),
]

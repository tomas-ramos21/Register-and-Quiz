from django.conf.urls import url, include
from login import views

#TEMPLATE TAGGING
app_name = 'login'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^user_login/$', views.user_login, name='user_login'),
]

"""reg_and_quiz URL Configuration

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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls import url
from django.urls import path

# Project Apps
from login import views as log
from lecturer import views as lecturer
from administrative import views as administrative
from student import views as student

urlpatterns = [
	url(r'^$', log.index, name='login'),
	url(r'^$', lecturer.lect_home, name='Lect Home'),
	url(r'^$', administrative.admin_home, name='Admin Home'),
	path('admin/', admin.site.urls),
	url(r'^login/', include('login.urls')),
	url(r'^administrative/', include('administrative.urls')),
	url(r'^lecturer/', include('lecturer.urls')),
	url(r'^student/', include('student.urls')),
	url(r'^logout/$', log.user_logout, name='logout'),
]


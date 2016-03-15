from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^findgames$', views.findgames, name="findgames"),
	url(r'^findgames/$', views.findgames, name="findgames"),
	url(r'^index/$', views.index, name="index"),
	url(r'^players$', views.players, name="players"),
	url(r'^players/$', views.players, name="players"),
	url(r'^fantasy/$', views.fantasy, name="fantasy"),
	url(r'^fantasy$', views.fantasy, name="fantasy"),
   	url(r'^stats$', views.stats, name="stats"),
	url(r'', views.index, name="index"),
]

urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^findgames$', views.findgames, name="findgames"),
	url(r'^index/$', views.index, name="index"),
	url(r'^findresults$', views.findresults, name="findresults"),
	url(r'^players/$', views.players, name="players"),
	url(r'^fantasy/$', views.fantasy, name="fantasy"),
	url(r'', views.index, name="index"),
]
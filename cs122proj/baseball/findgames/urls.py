from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^findgames/$', views.findgames),
	url(r'^players/$', views.players),
	url(r'^fantasy/$', views.fantasy),
]
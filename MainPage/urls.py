from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^main/$', views.main, name='main'),
    url(r'^results', views.results, name='results'),
    url(r'^person', views.person, name='person'),
    url(r'^tags', views.tags),
    url(r'^doubletags', views.doubletags),
    url(r'^about', views.about, name='about'),
    url(r'^doubleresults', views.doubleresults, name='doubleresults')
]

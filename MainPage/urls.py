from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^main/$', views.main, name='main'),
    url(r'^results', views.results, name='results'),
    url(r'^get_tags', views.get_tags),
]

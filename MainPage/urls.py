from django.conf.urls import patterns, url

urlpatterns = patterns('MainPage.views',
    url(r'^main/$', 'main', name='main'),
)
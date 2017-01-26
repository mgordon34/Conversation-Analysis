from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^main/', include('MainPage.urls')),
    url(r'^admin/', admin.site.urls),
]

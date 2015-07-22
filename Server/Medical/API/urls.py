from django.conf.urls import include, url
from django.contrib import admin
import API.views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^login',API.views.login),
    url(r'^logon',API.views.logon),
    url(r'^adddevice',API.views.adddevice),
    url(r'^deldevice',API.views.deldevice),
    url(r'^adddata',API.views.adddata),
    url(r'^getdata',API.views.getdata),

]

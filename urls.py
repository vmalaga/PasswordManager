from django.conf.urls.defaults import patterns, include, url
from passManager import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^send_email/(?P<idrow>\d+)/$', views.sendEmailView),
                       url(r'^send_email/(send)/$', views.sendEmailView),
                       url(r'^thanks/$', views.thanks),
    # Examples:
    # url(r'^$', 'PasswordManager.views.home', name='home'),
    # url(r'^PasswordManager/', include('PasswordManager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

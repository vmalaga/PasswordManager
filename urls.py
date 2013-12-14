from django.conf.urls.defaults import patterns, include, url
from passManager import views
from passManager.views import sendPassEmailView, mailsent
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^send_pass/(?P<rowid>\d+)/$', sendPassEmailView),
                       url(r'^send_pass/(send)/$', sendPassEmailView),
                       url(r'^mailsent/$', mailsent),
		       url(r'^$', lambda x: HttpResponseRedirect('/admin/passManager/passdb/')),
                       url(r'^admin/', include(admin.site.urls)),
)

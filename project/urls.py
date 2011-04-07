from django.conf.urls.defaults import patterns, include, url

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Akshai's main page
    url(r'^$', 'savegame.views.mainpage', name='mainpage'),
    
    # Temporary url for seeing logged in page. To be removed.
    url(r'^main/$', 'savegame.views.mainpageauth', name='mainpageauth'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Eudis's settings page
    url(r'settings/', 'savegame.views.settings'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

#urlpatterns += staticfiles_urlpatterns()


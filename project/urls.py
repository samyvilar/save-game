from django.conf.urls.defaults import patterns, include, url

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'savegame.views.mainpage'),
                       url(r'^registration/$', 'savegame.views.regpage'),
                       url(r'^registration/thanks/$', 'savegame.views.regthanks'),

                       url(r'settings/', 'savegame.views.settings'),
                       url(r'sign[Ii]n/', 'savegame.views.signIn'),
                       url(r'sign[Oo]ut/', 'savegame.views.signOut'),
                       url(r'gamepage/', 'savegame.views.gamepage'),
                       url(r'results/', 'savegame.views.results'),
                       
                       url(r'getvotedata/', 'savegame.views.getvotedata'),
                       url(r'getUploadedFileData/', 'savegame.views.getUploadedFileData'),
                       url(r'getCommentData/', 'savegame.views.getCommentData'),
                                         
                       url(r'^profile/(?P<user_id>\d*)/$', 'savegame.views.profile'),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       
)

#urlpatterns += staticfiles_urlpatterns()

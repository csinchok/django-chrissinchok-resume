from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','chrissinchok_resume.views.resume'),
    (r'^admin/', include(admin.site.urls)),
)
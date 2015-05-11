from django.conf.urls import include, url
from django.contrib import admin
from pics.views import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'trip.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/new/', csrf_exempt(RegisterJob.as_view()), name="api"), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
]

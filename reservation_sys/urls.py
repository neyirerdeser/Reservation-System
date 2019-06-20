from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'reservation_sys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^list/', include('booking.urls', namespace='booking')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

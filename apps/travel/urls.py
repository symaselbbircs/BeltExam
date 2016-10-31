from django.conf.urls import url, include
from . import views as v

urlpatterns = [
    url(r'^$', v.index, name="travel-index"),
    url(r'^/destination/(?P<destid>\d*)/$', v.destination, name="travel-destination"),
    url(r'^/add/$', v.addtrip, name="travel-add"),
    url(r'/addtotrip/(?P<destid>\d*)/$', v.usertrip, name='travel-tripadd')
]

from django.conf.urls import url
from . import views as v

urlpatterns = [
    url(r'^$', v.index, name="login-main"),
    url(r'^register$', v.register, name="login-register"),
    url(r'^login$', v.login, name="login-login"),
    url(r'^logout$', v.logout, name="logout")
]

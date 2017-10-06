from django.conf.urls import url
from . import views

urlpatterns = [
    # will be called if string is empty
    url(r'^$', views.index, name='index'),
]
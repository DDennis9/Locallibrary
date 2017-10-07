from django.conf.urls import url
from . import views

urlpatterns = [
    # will be called if string is empty
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'), # matches agains 'book/' followed
    # digits, digits are stored in a variable called pk.
]
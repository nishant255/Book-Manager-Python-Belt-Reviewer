from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^registration$', views.registration),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_book$', views.add_book),
    url(r'^adding_book$', views.adding_book),
    url(r'^books/(?P<book_id>\d+)$', views.view_book, name = 'view_book'),
    url(r'^show/user/(?P<user_id>\d+)$', views.view_user, name= 'view_user'),
    url(r'^books/adding_review/(?P<book_id>\d+)$', views.adding_review, name = 'adding_review'),
]

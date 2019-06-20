from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.SeatingView.as_view(), name='seating'),
    url(r'^(?P<pk>[0-9]+)/menu/$', views.MenuView.as_view(), name='menu'),
    url(r'^(?P<restaurant_id>[0-9]+)/reserve/$', views.reserve, name='reserve'),
    url(r'^(?P<restaurant_id>[0-9]+)/done/$', views.done, name='done'),
    # url(r'^(?P<pk>[0-9]+)/owner/$', views.OwnerView.as_view(), name='owner'),
    url(r'^(?P<user_id>[0-9]+)/owner/$', views.owner, name='owner'),
    url(r'^(?P<restaurant_id>[0-9]+)/menu_add/$', views.menu_add, name='menu_add'),
    url(r'^(?P<restaurant_id>[0-9]+)/menu_add_save/$', views.menu_add_save, name='menu_add_save'),
    url(r'^(?P<restaurant_id>[0-9]+)/menu_delete/$', views.menu_delete, name='menu_delete'),
    url(r'^(?P<restaurant_id>[0-9]+)/menu_delete_save/$', views.menu_delete_save, name='menu_delete_save'),
    url(r'^(?P<restaurant_id>[0-9]+)/table_add/$', views.table_add, name='table_add'),
    url(r'^(?P<restaurant_id>[0-9]+)/table_add_save/$', views.table_add_save, name='table_add_save'),
    url(r'^(?P<restaurant_id>[0-9]+)/table_delete/$', views.table_delete, name='table_delete'),
    url(r'^(?P<restaurant_id>[0-9]+)/table_delete_save/$', views.table_delete_save, name='table_delete_save'),
    url(r'^(?P<reservation_id>[0-9]+)/(?P<restaurant_id>[0-9]+)/cancel_reservation/$', views.cancel_reservation, name='cancel'),
]
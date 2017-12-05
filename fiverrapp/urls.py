from django.conf.urls import url
from .views import (home, login_view, register_view, logout_view, create_gig)

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    # url(r'^my_gigs/$', my_gigs, name='my_gigs'),
    url(r'^create_gig/$', create_gig, name='create_gig'),
    # url(r'^edit_gig/(?P<id>[0-9]+)/$', edit_gig, name='edit_gig'),
    # url(r'^gigs/(?P<id>[0-9]+)/$', views.gig_detail, name='gig_detail'),
]

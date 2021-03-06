from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^availability/all/$', views.course_availability),
    url(r'^availability/days/$', views.days),
    url(r'^availability/times/$', views.utc_times),
    url(r'^availability/$', views.user_availability),
    url(r'^availability/update/$', views.update_availability),

    url(r'^roles/all', views.study_roles),
    url(r'^roles/$', views.user_roles),
    url(r'^roles/update/$', views.update_role)
]

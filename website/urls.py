from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.home,                name='home'),
    path('login/',                        views.login_view,           name='login'),
    path('signup/',                       views.signup_view,          name='signup'),
    path('logout/',                       views.logout_view,          name='logout'),
    path('profile/',                      views.profile_view,         name='profile'),
    path('about/',                        views.about,               name='about'),
    path('careers/',                      views.jobs,                name='jobs'),
    path('careers/<int:pk>/',             views.job_detail,          name='job_detail'),
    path('careers/applied/',              views.application_success, name='application_success'),
    path('contact/',                      views.contact,             name='contact'),
    path('contact/thank-you/',            views.contact_success,     name='contact_success'),
    path('terms-and-conditions/',         views.terms,               name='terms'),
]

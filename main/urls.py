from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('admission/', views.admission, name='admission'),
    path('activities/', views.activities, name='activities'),
    path('announcements/', views.announcements, name='announcements'),
    path('fees/', views.fees, name='fees'),
    path('contact/', views.contact, name='contact'),
]
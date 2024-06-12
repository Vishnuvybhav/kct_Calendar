from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
   path('',views.login,name='login'),
   path('logout/', views.logout, name='logout'),
   path('show_calendar', views.show_calendar, name='show_calendar'),
   path('add_events/', views.add_event, name='add_event'),
   path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
   path('add_collaborators',views.add_collaborators,name='add_collaborators')
   
]
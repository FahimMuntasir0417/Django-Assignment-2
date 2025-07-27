from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.home, name='home'),
    path('participant/', views.participant_dashboard, name='participant'),
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp'),
    path('events/<int:event_id>/cancel-rsvp/', views.cancel_rsvp, name='cancel_rsvp'),
    path('dashboard/', views.manager_dashboard, name='dashboard'),

    path('events_list/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.create_event, name='event_create'),
    path('events/<int:pk>/update/', views.update_event, name='event_update'),
    path('events/<int:pk>/delete/', views.delete_event, name='event_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('p_category/', views.participant_catagory, name='participant_category'),
    path('p_event/', views.participant_event, name='participant_event'),
    path('main-dashboard/', views.main_dashboard, name='main-dashboard'),
]

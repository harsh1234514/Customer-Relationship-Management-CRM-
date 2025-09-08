from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Company URLs
    path('companies/', views.company_list, name='company_list'),
    path('companies/add/', views.company_create, name='company_create'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    path('companies/<int:pk>/edit/', views.company_edit, name='company_edit'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),

    # Contact URLs
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/add/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),

    # Lead URLs
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/add/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('leads/<int:pk>/delete/', views.lead_delete, name='lead_delete'),

    # Deal URLs
    path('deals/', views.deal_list, name='deal_list'),
    path('deals/add/', views.deal_create, name='deal_create'),
    path('deals/<int:pk>/', views.deal_detail, name='deal_detail'),
    path('deals/<int:pk>/edit/', views.deal_edit, name='deal_edit'),
    path('deals/<int:pk>/delete/', views.deal_delete, name='deal_delete'),

    # Activity URLs
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/add/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activities/<int:pk>/edit/', views.activity_edit, name='activity_edit'),
    path('activities/<int:pk>/complete/', views.activity_complete, name='activity_complete'),
    path('activities/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
]

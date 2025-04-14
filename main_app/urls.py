from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard), 
    path('licenses/', views.LicenseList.as_view(), name='license-index'),
    path('licenses/<int:pk>/', views.LicenseDetail.as_view(), name='license-detail'),
    path('licenses/create/', views.LicenseCreate.as_view(), name='license-create'),
    path('licenses/<int:pk>/update/', views.LicenseUpdate.as_view(), name='license-update'),
    path('licenses/<int:pk>/delete/', views.LicenseDelete.as_view(), name='license-delete'),
    path('checklists/', views.ChecklistList.as_view(), name='checklist-index'),
    path('checklists/create/', views.ChecklistCreate.as_view(), name='checklist-create'),
    path('checklists/<int:pk>/', views.ChecklistDetail.as_view(), name='checklist-detail'),
    path('checklists/<int:pk>/update/', views.ChecklistUpdate.as_view(), name='checklist-update'),
    path('checklists/<int:pk>/delete/', views.ChecklistDelete.as_view(), name='checklist-delete'),
    path('accounting/', views.AccountantList.as_view(), name='accountant-index'),
    path('accounting/create/', views.AccountantCreate.as_view(), name='accountant-create'),
    path('accounting/<int:pk>/', views.AccountantDetail.as_view(), name='accountant-detail'),
    path('accounting/<int:pk>/update/', views.AccountantUpdate.as_view(), name='accountant-update'),
    path('accounting/<int:pk>/delete/', views.AccountantDelete.as_view(), name='accountant-delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
from django.contrib import admin
from django.urls import path, include


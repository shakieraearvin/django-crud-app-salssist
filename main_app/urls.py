from django.urls import path
from . import views

urlpatterns = [
    path('licenses/', views.LicenseList.as_view(), name='license-index'),
    path('licenses/<int:pk>/', views.LicenseDetail.as_view(), name='license-detail'),
    path('licenses/create/', views.LicenseCreate.as_view(), name='license-create'),
    path('licenses/<int:pk>/update/', views.LicenseUpdate.as_view(), name='license-update'),
    path('licenses/<int:pk>/delete/', views.LicenseDelete.as_view(), name='license-delete'),
    path('accounts/signup/', views.signup, name='signup'),
]

from django.urls import path
from django.contrib import admin
from django.urls import path, include
from business import views

urlpatterns = [
    path('lk/', views.lk),
    path('business_company_info/', views.business_company_info),
    path('find_business_center/', views.find_business_center),
    path('set_office_in_bs/', views.set_office_in_bs),
    path('select_pc/', views.select_pc),
    path('cart/', views.cart_show),
    path('excel_dump/', views.excel_dump)
]

from django.urls import path, include

from auth_custom import views

urlpatterns = [
    path('login/', views.login),
    path('logout', views.logout),

    path(
        'registration/', include([
            path('company/', views.registration_company),
            path('investor/', views.registration_investor)
        ])
    ),
]

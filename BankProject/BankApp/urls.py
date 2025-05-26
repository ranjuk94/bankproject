"""
URL configuration for BankProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('registration/', views.register, name='registration'),
    path('home/', views.home, name='home'),
    path('view_users/', views.view_users, name='view_users'),
    path('banker_home/', views.banker_home, name='banker_home'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('banker/profile/<int:user_id>/', views.profile_view, name='banker_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('customer/<str:account_number>/transaction_history/', views.customer_transaction_history, name='transaction_history'),
    path('more/',views.more_details, name='more'),

]

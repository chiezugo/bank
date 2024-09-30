"""react URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from .views import (
    user_dashboard_view,
    card_view,
transactions_view,
settings_view,
    LoginView,
    logout_view,
    transfer_view,
    user_dashboard,
    bank_create_view,
    user_transfer_view,
    transfer_update_view,
    transfer_delete_view,
    admin_transfer_list_view,
    transaction_delete_view,
    request_fund_view,

profile_update_view,
create_card_view,
change_pin_view,
manage_view,
insurance_view,
location_view,
main_home_view

)

app_name = 'api'
urlpatterns = [
    path("en", main_home_view, name="home"),
    path('dashboard', user_dashboard_view, name='dashboard'),
    path('card', card_view, name='card'),
    path('manage', manage_view, name='manage'),
    path('locations', location_view, name='locations'),
    path('insurance', insurance_view, name='insurance'),
    path('change-pin', change_pin_view, name='change-pin'),
    path('setting', settings_view, name='setting'),
    path('transactions', transactions_view, name='transactions'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('newcard', create_card_view, name='newcard'),
    path('transfer/', transfer_view, name='transfer-view'),
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
    path('bank/', bank_create_view, name='bank-view'),
    path('transactions', transactions_view, name='transactions'),
    path('user-transfer/', user_transfer_view.as_view(), name='user-transfer'),
    path('update/<int:id>/', transfer_update_view, name='update-item'),
    path('delete/<int:id>/', transfer_delete_view, name='delete-item'),
    path('admin-transfer-list/', admin_transfer_list_view, name='admin-transfer-list'),
    path('delete/<int:id>/', transfer_delete_view, name='delete-item'),
    path('transactions/delete/<int:id>/', transaction_delete_view, name='transaction-item'),
    path('request-fund/', request_fund_view, name='request-fund'),
    path('profile-update/', profile_update_view, name='profile-update'),

]

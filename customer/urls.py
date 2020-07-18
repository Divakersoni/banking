"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from customer import views

urlpatterns = [
    # add account
    path('account_details/', views.FirstTrail.as_view()),
    # add transaction details
    path('account_transaction/', views.SecondTrail.as_view()),
    # get transaction history and account information
    path('account_enquiry/<int:account_number>/', views.ThirdTrail.as_view()),
    # get the excel url to download the file
    path('account_detail_manager/', views.FourthTrail.as_view()),
]

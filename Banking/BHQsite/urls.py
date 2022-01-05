from django.urls import path
from . import views


urlpatterns=[

    path('BHQ/<int:id>', views.BHQ, name="BHQ"),
    path('BHQfeed', views.BHQfeed, name="BHQfeed"),
    path('BHQdash',views.BHQdash, name='BHQdash'),
    path('BalanceSheet',views.BalanceSheet,name='BalanceSheet'),
    path('Balanceprocess',views.Balanceprocess,name='Balanceprocess'),
    path('Deposits',views.Deposits,name='Deposits'),
    path('Surplus',views.surplus,name='surplus'),
    path('Requestform',views.request1,name='request1'),
    path('Notifications',views.notification,name='notification'),
    path('BranchEfficiency',views.branch_efficiency,name='branch_efficiency'),
    path('BHQProfile',views.BHQ_profile,name='BHQ_profile'),
    path('delete',views.delete,name='delete')




]
from django.urls import path
from . import views
from . import models


urlpatterns=[


    path('Bankinfo/<int:id>',views.Bankinfo,name='Bankinfo'),
    path('BMsheet',views.BMsheet,name='BMsheet'),
    path('sheetprocess',views.sheetprocess,name='sheetprocess'),
    path('sheetdone',views.sheetdone,name='sheetdone'),
    path('Report_issue',views.requestform,name='requestform'),
    path('Notifications',views.bm_notification,name='bm_notification'),
    path('BMdash',views.BMdash,name='BMdash'),
    path('BMProfile',views.bm_profile,name='bm_profile')



]
from django.urls import path

from . import views

app_name='pi_visitors'

urlpatterns = [
    path('', views.visitors,name='visitors'),
    path('chooseDate', views.choose_date, name='chooseDate')
]



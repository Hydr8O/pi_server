from django.urls import path

from . import views

app_name='pi_visitors'

urlpatterns = [
    path('', views.visitors,name='visitors')
]



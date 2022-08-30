from . import views
from django.urls import path

app_name = 'proc_deals'

urlpatterns = [
    path('', views.start_page, name='start'),
    path('result/', views.result, name='result'),
]
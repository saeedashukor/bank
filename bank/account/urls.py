from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('deposit', views.deposit, name='deposit'),
    path('transfer/', views.transfer, name='transfer')
]
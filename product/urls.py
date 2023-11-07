from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductList.as_view(), name='list')
]

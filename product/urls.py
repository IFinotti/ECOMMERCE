from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    path('removefromcart/', views.RemoveFromCart.as_view(),
         name='removefromcart'),
    path('purchasesummary/', views.PurchaseSummary.as_view(), name='purchaseSummary'),
    path('addtocart/', views.AddToCart.as_view(), name='addtocart'),
    path('<slug>', views.ProductDetail.as_view(), name='detail'),
    path('', views.ProductList.as_view(), name='list'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('search/', views.Search.as_view(), name='search'),
]

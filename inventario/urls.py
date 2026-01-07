from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('services/', views.services, name='services'),
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/categoria/<int:category_id>/', views.productos_list, name='productos_by_category'),
    path('productos/create/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/add/', views.add_to_cart, name='add_to_cart'),
    path('productos/<int:pk>/delete/', views.producto_delete, name='producto_delete'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<int:pk>/', views.checkout_success, name='checkout_success'),
    path('tickets/historial/', views.historial_tickets, name='historial_tickets'),
    path('tickets/<int:pk>/canjear/', views.marcar_canjeado, name='marcar_canjeado'),
]

from django.urls import path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('search/', views.search_view, name='search'),
    path('product/<int:product_id>/', views.product_details, name='product-details'),
    path('contact/', views.contact, name='contact'),
	path('products/', views.product_list, name='product_list'),
	path('privacy policy/',views.privacy_policy, name='privacy_policy'),
	path('payment methoth/',views.payment_methoth,name='payment methoth'),
	path('Our_services/',views.Our_services,name='Our_services'),
	path('account_info/',views.account_info,name='account_info'),
]


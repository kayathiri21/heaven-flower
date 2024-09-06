"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('product/<int:product_id>',views.product_details,name='productd'),
    path('wishlist/',views.view_wishlist,name='wishlist'),
    path('wishlist/<int:product_id>',views.add_wishlist,name='add_wishlist'),
    path('cart/',views.view_cart,name='cart'),
    path('remove_from_cart',views. remove_from_cart,name='remove_from_cart'),
    path('cart/<int:product_id>',views.add_to_cart,name='add_to_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('order_page/',views.order_page,name='order_page'),
    path('rejectorder/<int:item_id>/',views.rejectorder,name='rejectorder'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.loginview,name='login'),
     path('logout/',views.logoutview,name='logout'),
    path('search/', views.search, name='search'),
     
     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


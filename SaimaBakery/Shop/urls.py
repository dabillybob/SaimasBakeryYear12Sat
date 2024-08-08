from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


#define url patterns for app
urlpatterns = [
    path('', views.Shop, name="Shop"),
    path('Cart/', views.Cart, name='Cart'),
    path('Checkout/', views.Checkout, name='Checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
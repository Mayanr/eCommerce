from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.index),
    url(r'^products/category/(?P<cat_id>\d+)$', views.prods_category),
    url(r'^products/show/(?P<prod_id>\d+)$', views.prods_show),
    url(r'^addtoCart/(?P<prod_id>\d+)$', views.add_to_cart),
    url(r'^carts$', views.shopping_cart),
    url(r'^process_payment$', views.process_payment),
    url(r'^confirmation$', views.confirmation),
    url(r'^admin$', views.admin_login),
    url(r'^verify_admin$', views.verify_admin),
    url(r'^dashboard/orders$', views.dashboard_orders),
    url(r'^dashboard/prods$', views.dashboard_prods),
    url(r'^orders/show/(?P<order_id>\d+)$', views.orders_show),
    url(r'^add_prod$', views.add_prod)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.index),
    url(r'^products/category/(?P<cat_id>\d+)$', views.prods_category),
    url(r'^products/show/(?P<prod_id>\d+)$', views.prods_show),
    url(r'^addtoCart/(?P<prod_id>\d+)$', views.add_to_cart),
    url(r'^editCart/(?P<prod_id>\d+)$', views.edit_cart),
    url(r'^removeFromCart/(?P<prod_id>\d+)$', views.remove_from_cart),
    url(r'^empty_cart$', views.empty_cart),
    url(r'^cart_contents$', views.shopping_cart),
    url(r'^checkout$', views.checkout),
    url(r'^process_order$', views.process_order),
    url(r'^confirmation$', views.confirmation),
    url(r'^admin$', views.admin_login),
    url(r'^verify_admin$', views.verify_admin),
    url(r'^admin_logout$', views.admin_logout),
    url(r'^dashboard/orders$', views.dashboard_orders),
    url(r'^dashboard/prods$', views.dashboard_prods),
    url(r'^orders/show/(?P<order_id>\d+)$', views.orders_show),
    url(r'^orders/update/(?P<order_id>\d+)$', views.update_order_status),
    url(r'^add_prod$', views.add_prod),
    url(r'^dashboard/delete/(?P<prod_id>\d+)$', views.delete_prod),
    url(r'^update_prod$', views.update_prod)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
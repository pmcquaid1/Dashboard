from django.urls import path
from . import test_views

urlpatterns = [
    path("test_home/", test_views.test_home, name="test_home"),
    path("ping/", test_views.ping),
    path("healthcheck/", test_views.healthcheck),
    path("shipment_test/", test_views.shipment_test),
    path("document_test/", test_views.document_test),
    path("routes/", test_views.list_routes),
]

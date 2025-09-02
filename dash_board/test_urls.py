from django.urls import path
from . import test_views
from dash_board.test_views import ping_view
from .decorators import log_test_access, dry_run_safe

urlpatterns = [
    # HTML pages for manual testing
    path('test/shipment/', test_views.shipment_test, name='shipment_test'),
    path('test/document/', test_views.document_test, name='document_test'),
    path('test-template/', test_views.test_template_render),

    # API endpoints with audit logging and dry-run support
    path(
        'api/test/ping',
        log_test_access(dry_run_safe(ping_view)),
        name='ping'
    ),
    path(
        'api/test/shipment/',
        log_test_access(dry_run_safe(test_views.receive_shipment_xml)),
        name='receive_shipment_xml'
    ),
    path(
        'api/test/document/',
        log_test_access(dry_run_safe(test_views.receive_document_xml)),
        name='receive_document_xml'
    ),
    path(
        'api/test/status/',
        log_test_access(dry_run_safe(test_views.status_view)),
        name='status_view'
    ),
]

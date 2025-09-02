import logging
import xml.etree.ElementTree as ET
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def status_view(request):
    config_snapshot = {
        'APP_MODE': getattr(settings, 'APP_MODE', 'undefined'),
        'ENV': getattr(settings, 'ENV', 'undefined'),
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
    }
    headers = {
        'X-Contact-Email': request.headers.get('X-Contact-Email'),
        'X-Access-Token': request.headers.get('X-Access-Token'),
        'User-Agent': request.headers.get('User-Agent'),
    }
    response = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'path': request.path,
        'method': request.method,
        'config': config_snapshot,
        'headers': headers,
        'remote_ip': request.META.get('REMOTE_ADDR'),
    }
    return JsonResponse(response)

def ping_view(request):
    contact = getattr(request, 'vendor_contact', 'unknown')
    return JsonResponse({
        'status': 'ok',
        'contact': contact,
        'mode': getattr(request, 'APP_MODE', 'unknown')
    })

@csrf_exempt
def test_payload_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        xml_data = request.body.decode('utf-8')
        root = ET.fromstring(xml_data)
    except Exception as e:
        logger.exception("[TEST_API] ❌ Failed to parse XML")
        return JsonResponse({'error': 'Invalid XML payload'}, status=400)

    if request.path.endswith('/shipment/'):
        payload_type = 'shipment'
        identifier = root.findtext('ShipmentID')
    elif request.path.endswith('/document/'):
        payload_type = 'document'
        identifier = root.findtext('DocumentID')
    else:
        logger.warning(f"[TEST_API] ❓ Unknown endpoint: {request.path}")
        return JsonResponse({'error': 'Unknown endpoint'}, status=404)

    logger.info(f"[TEST_API] ✅ {payload_type.capitalize()} received: {identifier}")

    if settings.DRY_RUN_MODE:
        logger.debug(f"[TEST_API] 🚫 Dry-run mode: skipping DB write for {payload_type} {identifier}")
    else:
        logger.debug(f"[TEST_API] ✅ {payload_type.capitalize()} {identifier} would be saved")

    return JsonResponse({'status': 'success', 'type': payload_type, 'id': identifier})

@csrf_exempt
def shipment_test(request):
    return test_payload_view(request)

@csrf_exempt
def document_test(request):
    return test_payload_view(request)

def test_template_render(request):
    return render(request, 'shipment_test.html')

@csrf_exempt
def receive_shipmentxml(request):
    return test_payload_view(request)

@csrf_exempt
def receive_documentxml(request):
    return test_payload_view(request)



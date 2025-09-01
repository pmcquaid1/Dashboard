from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def test_home(request):
    return render(request, "test_home.html")

def test_home(request):
    logger.info("Test home accessed from %s", request.META.get("REMOTE_ADDR"))

    banner = ""
    if getattr(settings, "DRY_RUN_MODE", False):
        banner = "<div style='background:#ffc;padding:10px;text-align:center;'>⚠️ Test Environment – Data may be reset</div>"

    return HttpResponse(f"""
        {banner}
        <h1>Welcome to SLLHub Test Environment</h1>
        <p>This is a safe space for dry-run testing and vendor validation.</p>
    """)


def ping(request):
    return HttpResponse("pong")
def ping(request):
    return HttpResponse("✅ Django is running and routing is working.")

def healthcheck(request):
    return HttpResponse("OK")

def shipment_test(request):
    return JsonResponse({"status": "shipment test passed"})

def shipment_test(request):
    return render(request, 'shipment_test.html')

def document_test(request):
    return render(request, 'document_test.html')



def document_test(request):
    logger.warning("📍 document_test view executed")
    return HttpResponse("✅ document_test view executed")

def document_test(request):
    return JsonResponse({"status": "document test passed"})

def list_routes(request):
    return JsonResponse({
        "routes": [
            "test_home/",
            "ping/",
            "healthcheck/",
            "shipment_test/",
            "document_test/",
            "routes/"
        ]
    })

def list_routes(request):
    urls = [str(p.pattern) for p in get_resolver().url_patterns]
    return JsonResponse({"routes": urls})

print("✅ views.py loaded")

logger = logging.getLogger(__name__)
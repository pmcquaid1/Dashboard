class TestModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("✅ TestModeMiddleware initialized")

    def __call__(self, request):
        print("✅ TestModeMiddleware called")
        request.APP_MODE = "test"
        return self.get_response(request)


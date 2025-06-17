from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dash_board.urls')),  # ✅ This line connects your app's URLs
]


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('common.urls')),
    path('api/', include('assessments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [path("admin/", admin.site.urls), path("", include("meetup.urls"))]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

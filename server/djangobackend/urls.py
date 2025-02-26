"""djangobackend URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # the path below, remove djangoapp and leave quotes empty
    path('djangoapp/', include('djangoapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

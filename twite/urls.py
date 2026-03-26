from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.urls import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('tweet/', permanent=True)),
    path('tweet/',include('tweet.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
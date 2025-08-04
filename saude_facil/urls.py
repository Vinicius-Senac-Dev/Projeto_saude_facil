from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tela_login.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('tela_principal/', include('tela_principal.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
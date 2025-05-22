from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tela_principal/', include('tela_principal.urls')),
    path('', include('tela_principal.urls')),  # Adicione esta linha
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
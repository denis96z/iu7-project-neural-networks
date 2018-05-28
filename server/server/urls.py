from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api.serializers import router
from server.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('api-browser/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

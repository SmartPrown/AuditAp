from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login, name="log_in")
    , path('direct_file', views.direct_file, name="direct_file")
    , path('log_out', views.log_out, name="log_out")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

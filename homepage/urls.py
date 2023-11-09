from django.conf.urls.static import static
from django.urls import include, path

from TTS import settings
from . import views

app_name = "homepage"
urlpatterns = [
    path("text/", views.TextClass.as_view(), name="text"),
    path("file/", views.FileClass.as_view(), name="file"),
    path(
        "processing/<int:user_id>/<str:upload_time>/",
        views.ProcessingClass.as_view(),
        name="processing",
    ),
    path(
        "is_processed/<int:user_id>/<str:upload_time>/",
        views.is_processed,
        name="is_processed",
    ),
    path("userhistory/", views.user_history, name="user_history"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

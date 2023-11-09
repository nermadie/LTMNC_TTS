from django.urls import include, path
from . import views

app_name = "user"
urlpatterns = [
    path("", views.IndexClass.as_view(), name="index"),
]

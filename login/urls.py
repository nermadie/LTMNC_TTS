from django.urls import include, path

from . import views

app_name = "login"
urlpatterns = [
    path("", views.LoginClass.as_view(), name="login"),
    path("register/", views.RegisterClass.as_view(), name="register"),
    path("logout/", views.logout_view, name="logout"),
]

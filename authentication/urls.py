from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views

app_name = 'auth'

router = DefaultRouter()
router.register("", views.SignUpUserAPI, basename="sign-up")

urlpatterns = [
    path("sign-up", include(router.urls)),
    path("login", views.LoginUserApi.as_view(), name="login"),
]
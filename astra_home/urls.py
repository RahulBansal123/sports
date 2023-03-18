from django.urls import include, re_path, path
from . import views

app_name = "astra_home"

urlpatterns = [
    re_path(r"emptyCart/", views.getEmptyCart, name="getEmptyCart"),
    re_path(r"logout/", views.getLogOut, name="getLogout"),
    re_path(r"addToCart/", views.addToCart, name="addToCart"),
    re_path(r"removeFromCart/", views.removeFromCart, name="removeFromCart"),
    re_path(r"cart/", views.getCartView, name="getHello"),
    re_path(r"login/", views.getLogin, name="getLogin"),
    re_path(r"verifyOtp/", views.getOtp, name="getOtp"),
    re_path(r"register/", views.registerView, name="getRegistrationView"),
    re_path(r"signup/", views.getRegister, name="getRegister"),
    re_path(r"temp/", views.getTempView, name="getTempView"),
    re_path(r"", views.homeView, name="getHomeView"),
]

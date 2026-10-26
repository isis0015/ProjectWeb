from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.AgroLoginView.as_view(), name="login"),
    path("registro/", views.RegistroView.as_view(), name="registro"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("recuperar/", auth_views.PasswordResetView.as_view(
        template_name="cuentas/recuperar.html",
        email_template_name="cuentas/email_recuperar.txt",
        subject_template_name="cuentas/email_recuperar_asunto.txt",
    ), name="password_reset"),
    path("recuperar/enviado/", auth_views.PasswordResetDoneView.as_view(
        template_name="cuentas/recuperar_enviado.html"), name="password_reset_done"),
    path("recuperar/completado/", auth_views.PasswordResetCompleteView.as_view(
        template_name="cuentas/restablecer_completo.html"), name="password_reset_complete"),
    path("recuperar/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="cuentas/restablecer.html"), name="password_reset_confirm"),
]
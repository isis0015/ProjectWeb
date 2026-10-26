from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": "tucorreo@ejemplo.com",
                                       "autocomplete": "email"}),
    )
    password = forms.CharField(
        label="Contraseña", strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Tu contraseña", "autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": "Correo o contraseña incorrectos.",
        "inactive": "Esta cuenta está desactivada.",
    }

    def clean_username(self):
        return self.cleaned_data["username"].lower()


class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("nombre", "apellidos", "email")
        labels = {"nombre": "Nombre(s)", "apellidos": "Apellidos", "email": "Correo electrónico"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["apellidos"].required = True
        self.fields["email"].widget.attrs.update({"placeholder": "tucorreo@ejemplo.com", "autocomplete": "email"})
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].help_text = "Mínimo 8 caracteres."
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["password2"].help_text = ""
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column("nombre", css_class="col-md-6"), Column("apellidos", css_class="col-md-6")),
            "email", "password1", "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email
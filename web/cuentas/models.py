from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("El correo es obligatorio")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("rol", Usuario.Rol.CLIENTE)
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("rol", Usuario.Rol.ADMIN)
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra)


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        CLIENTE = "cliente", "Cliente"
        ADMIN = "admin", "Administrador"

    email = models.EmailField("correo electrónico", unique=True)
    nombre = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.CLIENTE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.nombre} {self.apellidos}".strip()

    def get_short_name(self):
        return self.nombre

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        if self.rol == self.Rol.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)


class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="direcciones")
    alias = models.CharField(max_length=40, default="Casa")
    calle = models.CharField(max_length=150)
    numero_ext = models.CharField(max_length=15)
    numero_int = models.CharField(max_length=15, blank=True)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    referencias = models.CharField(max_length=200, blank=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = "dirección"
        verbose_name_plural = "direcciones"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario"], condition=models.Q(es_principal=True),
                name="una_direccion_principal_por_usuario",
            )
        ]

    def __str__(self):
        return f"{self.alias}: {self.calle} {self.numero_ext}, {self.colonia}"

    @property
    def completa(self):
        interior = f" Int. {self.numero_int}" if self.numero_int else ""
        return (f"{self.calle} {self.numero_ext}{interior}, {self.colonia}, "
                f"{self.ciudad}, {self.estado}, C.P. {self.codigo_postal}")

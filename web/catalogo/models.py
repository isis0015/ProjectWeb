from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    icono = models.CharField(max_length=40, default="bi-box-seam", help_text="Clase de Bootstrap Icons")
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    presentacion = models.CharField(max_length=60, blank=True, help_text="Ej. 1 L, 25 kg, pieza")
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="productos/", blank=True)
    # Atributos variables por tipo de producto:
    # {"ingrediente_activo": "...", "dosis": "...", "enfermedades_objetivo": ["antracnosis"], "material": "..."}
    atributos = models.JSONField(default=dict, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]
        indexes = [models.Index(fields=["activo", "categoria"])]

    def __str__(self):
        return self.nombre

    @property
    def disponible(self):
        return self.activo and self.stock > 0

    @property
    def enfermedades_objetivo(self):
        return self.atributos.get("enfermedades_objetivo", [])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nombre)
            slug, n = base, 2
            while Producto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Resena(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="resenas")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resenas")
    calificacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "reseña"
        verbose_name_plural = "reseñas"
        constraints = [
            models.UniqueConstraint(fields=["producto", "usuario"], name="una_resena_por_usuario_y_producto")
        ]

    def __str__(self):
        return f"{self.producto} · {self.calificacion}★"

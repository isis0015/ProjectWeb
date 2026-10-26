from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q
from django.views.generic import ListView, TemplateView

from .models import Categoria, Producto

ORDENES = {"recientes": "-creado", "precio_asc": "precio", "precio_desc": "-precio", "nombre": "nombre"}


def productos_activos():
    return (Producto.objects.filter(activo=True)
            .select_related("categoria")
            .annotate(promedio=Avg("resenas__calificacion"), num_resenas=Count("resenas")))


class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "catalogo/inicio.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.annotate(
            total=Count("productos", filter=Q(productos__activo=True)))
        ctx["destacados"] = productos_activos().filter(stock__gt=0)[:4]
        return ctx


class CatalogoView(LoginRequiredMixin, ListView):
    template_name = "catalogo/catalogo.html"
    context_object_name = "productos"
    paginate_by = 12

    def get_queryset(self):
        qs = productos_activos()
        q = self.request.GET.get("q", "").strip()
        cat = self.request.GET.get("categoria", "")
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
        if cat:
            qs = qs.filter(categoria__slug=cat)
        return qs.order_by(ORDENES.get(self.request.GET.get("orden"), "-creado"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx.update(
            categorias=Categoria.objects.all(),
            q=self.request.GET.get("q", "").strip(),
            categoria_actual=self.request.GET.get("categoria", ""),
            orden=self.request.GET.get("orden", "recientes"),
            querystring=params.urlencode(),
        )
        return ctx

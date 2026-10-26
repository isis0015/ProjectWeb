from django.core.management.base import BaseCommand

from catalogo.models import Categoria, Producto

CATEGORIAS = [
    ("Fertilizantes", "fertilizantes", "bi-flower2", "Nutrición para el árbol y el suelo", 1),
    ("Fungicidas", "fungicidas", "bi-shield-check", "Control de roña, antracnosis y más", 2),
    ("Herramientas", "herramientas", "bi-scissors", "Poda y manejo del huerto", 3),
    ("Riego", "riego", "bi-droplet-half", "Goteo, aspersión y accesorios", 4),
]

PRODUCTOS = [
    ("fertilizantes", "Fertilizante NPK 20-10-10", 890, 30, "25 kg",
     "Mezcla balanceada para etapa de crecimiento y producción.",
     {"ingrediente_activo": "Nitrógeno, fósforo y potasio", "dosis": "250 g por árbol cada 2 meses"}),
    ("fertilizantes", "Sulfato de zinc", 180, 48, "1 kg",
     "Corrige deficiencias de zinc en hoja, común en aguacate.",
     {"ingrediente_activo": "Sulfato de zinc", "dosis": "2 g/L en aspersión foliar"}),
    ("fertilizantes", "Humus de lombriz", 260, 25, "20 kg",
     "Mejorador orgánico que activa la vida del suelo.",
     {"ingrediente_activo": "Materia orgánica", "dosis": "2 kg por árbol al año"}),
    ("fungicidas", "Fungicida cúprico", 320.50, 45, "1 L",
     "Protección preventiva y curativa contra enfermedades fúngicas.",
     {"ingrediente_activo": "Oxicloruro de cobre", "dosis": "2 ml/L",
      "enfermedades_objetivo": ["antracnosis", "roña"]}),
    ("fungicidas", "Mancozeb 80 WP", 410, 22, "1 kg",
     "Fungicida de contacto de amplio espectro.",
     {"ingrediente_activo": "Mancozeb", "dosis": "2.5 g/L",
      "enfermedades_objetivo": ["antracnosis", "roña"]}),
    ("fungicidas", "Azoxistrobina 250 SC", 780, 0, "500 ml",
     "Fungicida sistémico para brotes de antracnosis.",
     {"ingrediente_activo": "Azoxistrobina", "dosis": "0.5 ml/L",
      "enfermedades_objetivo": ["antracnosis"]}),
    ("herramientas", "Tijeras de podar profesionales", 340, 18, "Pieza",
     "Hoja de acero al carbono con mango ergonómico.", {"material": "Acero al carbono"}),
    ("herramientas", "Podadora telescópica", 690, 12, "3 m",
     "Alcanza ramas altas sin necesidad de escalera.", {"material": "Aluminio"}),
    ("riego", "Kit de riego por goteo", 1250, 9, "100 m",
     "Manguera, goteros y conectores para huerto pequeño.", {"material": "Polietileno"}),
    ("riego", "Aspersor de impacto", 95, 60, '1/2"',
     "Cobertura circular ajustable de hasta 12 m.", {"material": "Latón"}),
]


class Command(BaseCommand):
    help = "Carga categorías y productos de ejemplo"

    def handle(self, *args, **options):
        cats = {}
        for nombre, slug, icono, desc, orden in CATEGORIAS:
            cats[slug], _ = Categoria.objects.update_or_create(
                slug=slug, defaults={"nombre": nombre, "icono": icono, "descripcion": desc, "orden": orden})
        for cat, nombre, precio, stock, pres, desc, attrs in PRODUCTOS:
            Producto.objects.update_or_create(
                nombre=nombre,
                defaults={"categoria": cats[cat], "precio": precio, "stock": stock,
                          "presentacion": pres, "descripcion": desc, "atributos": attrs, "activo": True})
        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados"))
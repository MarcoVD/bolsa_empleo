# usuarios/management/commands/crear_categorias.py
# Crear la estructura de directorios: usuarios/management/commands/

from django.core.management.base import BaseCommand
from usuarios.models import Categoria


class Command(BaseCommand):
    help = 'Crea las categorías iniciales para las vacantes'

    def handle(self, *args, **options):
        categorias = [
            {
                'nombre': 'Tecnologías de la Información',
                'descripcion': 'Desarrollo de software, sistemas, redes, ciberseguridad, etc.'
            },
            {
                'nombre': 'Marketing y Ventas',
                'descripcion': 'Marketing digital, ventas, publicidad, relaciones públicas, etc.'
            },
            {
                'nombre': 'Recursos Humanos',
                'descripcion': 'Gestión de talento, reclutamiento, capacitación, nómina, etc.'
            },
            {
                'nombre': 'Finanzas y Contabilidad',
                'descripcion': 'Contabilidad, auditoría, finanzas corporativas, análisis financiero, etc.'
            },
            {
                'nombre': 'Diseño y Multimedia',
                'descripcion': 'Diseño gráfico, web, multimedia, producción audiovisual, etc.'
            },
            {
                'nombre': 'Ingeniería',
                'descripcion': 'Ingeniería civil, industrial, mecánica, eléctrica, etc.'
            },
            {
                'nombre': 'Administración y Gestión',
                'descripcion': 'Administración general, gestión de proyectos, operaciones, etc.'
            },
            {
                'nombre': 'Educación y Capacitación',
                'descripcion': 'Docencia, capacitación corporativa, desarrollo educativo, etc.'
            },
            {
                'nombre': 'Salud y Medicina',
                'descripcion': 'Medicina, enfermería, servicios de salud, farmacia, etc.'
            },
            {
                'nombre': 'Legal y Jurídico',
                'descripcion': 'Derecho corporativo, litigio, asesoría legal, notaría, etc.'
            },
            {
                'nombre': 'Transporte y Logística',
                'descripcion': 'Logística, cadena de suministro, transporte, almacenamiento, etc.'
            },
            {
                'nombre': 'Servicio al Cliente',
                'descripcion': 'Atención al cliente, soporte técnico, call center, etc.'
            },
            {
                'nombre': 'Construcción y Arquitectura',
                'descripcion': 'Arquitectura, construcción, supervisión de obras, etc.'
            },
            {
                'nombre': 'Comunicación y Medios',
                'descripcion': 'Periodismo, comunicación corporativa, medios digitales, etc.'
            },
            {
                'nombre': 'Otros',
                'descripcion': 'Otras categorías no especificadas anteriormente'
            }
        ]

        created_count = 0
        for cat_data in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Categoría creada: {categoria.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Proceso completado. {created_count} categorías nuevas creadas.'
            )
        )
# usuarios/migrations/0003_agregar_vacantes_categorias.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0002_cambiar_apellidos_por_separado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Vacante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('tipo_empleo', models.CharField(choices=[('tiempo_completo', 'Tiempo Completo'), ('medio_tiempo', 'Medio Tiempo'), ('proyecto', 'Por Proyecto'), ('temporal', 'Temporal'), ('practicas', 'Prácticas Profesionales')], max_length=20)),
                ('modalidad', models.CharField(choices=[('presencial', 'Presencial'), ('remoto', 'Remoto'), ('hibrido', 'Híbrido')], default='presencial', max_length=15)),
                ('estado', models.CharField(choices=[('aguascalientes', 'Aguascalientes'), ('baja_california', 'Baja California'), ('baja_california_sur', 'Baja California Sur'), ('campeche', 'Campeche'), ('chiapas', 'Chiapas'), ('chihuahua', 'Chihuahua'), ('ciudad_de_mexico', 'Ciudad de México'), ('coahuila', 'Coahuila'), ('colima', 'Colima'), ('durango', 'Durango'), ('estado_de_mexico', 'Estado de México'), ('guanajuato', 'Guanajuato'), ('guerrero', 'Guerrero'), ('hidalgo', 'Hidalgo'), ('jalisco', 'Jalisco'), ('michoacan', 'Michoacán'), ('morelos', 'Morelos'), ('nayarit', 'Nayarit'), ('nuevo_leon', 'Nuevo León'), ('oaxaca', 'Oaxaca'), ('puebla', 'Puebla'), ('queretaro', 'Querétaro'), ('quintana_roo', 'Quintana Roo'), ('san_luis_potosi', 'San Luis Potosí'), ('sinaloa', 'Sinaloa'), ('sonora', 'Sonora'), ('tabasco', 'Tabasco'), ('tamaulipas', 'Tamaulipas'), ('tlaxcala', 'Tlaxcala'), ('veracruz', 'Veracruz'), ('yucatan', 'Yucatán'), ('zacatecas', 'Zacatecas')], max_length=30)),
                ('ciudad', models.CharField(max_length=100)),
                ('salario_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salario_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('detalles_salario', models.CharField(blank=True, help_text='Ej: A tratar, Según aptitudes, Más bonos', max_length=200, null=True)),
                ('fecha_inicio_estimada', models.DateField(blank=True, null=True)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_limite', models.DateField()),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('estado_vacante', models.CharField(choices=[('borrador', 'Borrador'), ('publicada', 'Publicada'), ('cerrada', 'Cerrada'), ('eliminada', 'Eliminada')], default='borrador', max_length=15)),
                ('aprobada', models.BooleanField(default=False)),
                ('destacada', models.BooleanField(default=False)),
                ('max_postulantes', models.IntegerField(choices=[(5, '5'), (10, '10'), (20, '20'), (50, '50')], default=20)),
                ('max_postulaciones_por_interesado', models.IntegerField(default=1)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacantes', to='usuarios.categoria')),
                ('reclutador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacantes', to='usuarios.reclutador')),
                ('secretaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacantes', to='usuarios.secretaria')),
            ],
            options={
                'verbose_name': 'Vacante',
                'verbose_name_plural': 'Vacantes',
                'ordering': ['-fecha_publicacion'],
            },
        ),
        migrations.CreateModel(
            name='RequisitoVacante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educacion_minima', models.CharField(blank=True, max_length=200, null=True)),
                ('experiencia_minima', models.CharField(blank=True, max_length=200, null=True)),
                ('descripcion_requisitos', models.TextField(help_text='Detalla los requisitos específicos, habilidades técnicas, etc.')),
                ('vacante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='requisitos', to='usuarios.vacante')),
            ],
            options={
                'verbose_name': 'Requisito de Vacante',
                'verbose_name_plural': 'Requisitos de Vacantes',
            },
        ),
    ]
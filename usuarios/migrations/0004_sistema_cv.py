# usuarios/migrations/0004_sistema_cv.py
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0003_agregar_vacantes_categorias'),
    ]

    operations = [
        # Hacer campos opcionales en Interesado (ya que ahora se llenan en el CV)
        migrations.AlterField(
            model_name='interesado',
            name='nombre',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='interesado',
            name='apellido_paterno',
            field=models.CharField(blank=True, max_length=50),
        ),

        # Crear modelo Curriculum
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resumen_profesional',
                 models.TextField(blank=True, help_text='Describe brevemente tu perfil y objetivos profesionales',
                                  null=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('interesado',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum',
                                      to='usuarios.interesado')),
            ],
            options={
                'verbose_name': 'Currículum',
                'verbose_name_plural': 'Currículums',
            },
        ),

        # Crear modelo ExperienciaLaboral
        migrations.CreateModel(
            name='ExperienciaLaboral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(max_length=200)),
                ('puesto', models.CharField(max_length=200)),
                ('descripcion', models.TextField(help_text='Funciones y responsabilidades principales')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('actual', models.BooleanField(default=False, help_text='Marca si es tu trabajo actual')),
                ('curriculum',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiencias',
                                   to='usuarios.curriculum')),
            ],
            options={
                'verbose_name': 'Experiencia Laboral',
                'verbose_name_plural': 'Experiencias Laborales',
                'ordering': ['-fecha_inicio'],
            },
        ),

        # Crear modelo Educacion
        migrations.CreateModel(
            name='Educacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text='Título obtenido o nivel educativo', max_length=200)),
                ('institucion', models.CharField(max_length=200)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción adicional', null=True)),
                ('curriculum',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educaciones',
                                   to='usuarios.curriculum')),
            ],
            options={
                'verbose_name': 'Educación',
                'verbose_name_plural': 'Educación y Formación',
                'ordering': ['-fecha_inicio'],
            },
        ),

        # Crear modelo Habilidad
        migrations.CreateModel(
            name='Habilidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                related_name='habilidades', to='usuarios.categoria')),
            ],
            options={
                'verbose_name': 'Habilidad',
                'verbose_name_plural': 'Habilidades',
                'ordering': ['nombre'],
            },
        ),

        # Crear modelo HabilidadInteresado
        migrations.CreateModel(
            name='HabilidadInteresado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(
                    choices=[('basico', 'Básico'), ('intermedio', 'Intermedio'), ('avanzado', 'Avanzado'),
                             ('experto', 'Experto')], max_length=15)),
                ('curriculum',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habilidades',
                                   to='usuarios.curriculum')),
                ('habilidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.habilidad')),
            ],
            options={
                'verbose_name': 'Habilidad del Interesado',
                'verbose_name_plural': 'Habilidades del Interesado',
            },
        ),

        # Crear modelo IdiomaInteresado
        migrations.CreateModel(
            name='IdiomaInteresado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idioma', models.CharField(max_length=50)),
                ('nivel_lectura', models.CharField(
                    choices=[('A1', 'A1 - Principiante'), ('A2', 'A2 - Elemental'), ('B1', 'B1 - Intermedio'),
                             ('B2', 'B2 - Intermedio Alto'), ('C1', 'C1 - Avanzado'), ('C2', 'C2 - Maestría'),
                             ('nativo', 'Nativo')], max_length=10)),
                ('nivel_escritura', models.CharField(
                    choices=[('A1', 'A1 - Principiante'), ('A2', 'A2 - Elemental'), ('B1', 'B1 - Intermedio'),
                             ('B2', 'B2 - Intermedio Alto'), ('C1', 'C1 - Avanzado'), ('C2', 'C2 - Maestría'),
                             ('nativo', 'Nativo')], max_length=10)),
                ('nivel_conversacion', models.CharField(
                    choices=[('A1', 'A1 - Principiante'), ('A2', 'A2 - Elemental'), ('B1', 'B1 - Intermedio'),
                             ('B2', 'B2 - Intermedio Alto'), ('C1', 'C1 - Avanzado'), ('C2', 'C2 - Maestría'),
                             ('nativo', 'Nativo')], max_length=10)),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idiomas',
                                                 to='usuarios.curriculum')),
            ],
            options={
                'verbose_name': 'Idioma del Interesado',
                'verbose_name_plural': 'Idiomas del Interesado',
            },
        ),

        # Agregar constraints unique_together
        migrations.AlterUniqueTogether(
            name='habilidadinteresado',
            unique_together={('curriculum', 'habilidad')},
        ),
        migrations.AlterUniqueTogether(
            name='idiomainteresado',
            unique_together={('curriculum', 'idioma')},
        ),
    ]
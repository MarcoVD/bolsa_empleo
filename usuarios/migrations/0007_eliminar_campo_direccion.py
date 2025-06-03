# usuarios/migrations/0007_eliminar_campo_direccion.py
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0006_actualizar_interesado_municipios_edomex'),
    ]

    operations = [
        # Eliminar el campo direccion del modelo Interesado
        migrations.RemoveField(
            model_name='interesado',
            name='direccion',
        ),
    ]
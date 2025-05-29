# usuarios/migrations/0006_actualizar_interesado_municipios_edomex.py
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0005_cambiar_estados_por_municipios_edomex'),
    ]

    operations = [
        # Agregar el nuevo campo municipio para Interesado
        migrations.AddField(
            model_name='interesado',
            name='municipio',
            field=models.CharField(
                blank=True,
                choices=[
                    ('acambay', 'Acambay'), ('acolman', 'Acolman'), ('aculco', 'Aculco'),
                    ('almoloya_de_alquisiras', 'Almoloya de Alquisiras'), ('almoloya_de_juarez', 'Almoloya de Juárez'),
                    ('almoloya_del_rio', 'Almoloya del Río'), ('amanalco', 'Amanalco'), ('amatepec', 'Amatepec'),
                    ('amecameca', 'Amecameca'), ('apaxco', 'Apaxco'), ('atenco', 'Atenco'), ('atizapan', 'Atizapán'),
                    ('atizapan_de_zaragoza', 'Atizapán de Zaragoza'), ('atlacomulco', 'Atlacomulco'),
                    ('atlautla', 'Atlautla'), ('axapusco', 'Axapusco'), ('ayapango', 'Ayapango'),
                    ('calimaya', 'Calimaya'), ('capulhuac', 'Capulhuac'),
                    ('coacalco_de_berriozabal', 'Coacalco de Berriozábal'), ('coatepec_harinas', 'Coatepec Harinas'),
                    ('cocotitlan', 'Cocotitlán'), ('coyotepec', 'Coyotepec'), ('cuautitlan', 'Cuautitlán'),
                    ('cuautitlan_izcalli', 'Cuautitlán Izcalli'), ('donato_guerra', 'Donato Guerra'),
                    ('ecatepec_de_morelos', 'Ecatepec de Morelos'), ('ecatzingo', 'Ecatzingo'), ('el_oro', 'El Oro'),
                    ('huehuetoca', 'Huehuetoca'), ('hueypoxtla', 'Hueypoxtla'), ('huixquilucan', 'Huixquilucan'),
                    ('isidro_fabela', 'Isidro Fabela'), ('ixtapaluca', 'Ixtapaluca'),
                    ('ixtapan_de_la_sal', 'Ixtapan de la Sal'), ('ixtapan_del_oro', 'Ixtapan del Oro'),
                    ('ixtlahuaca', 'Ixtlahuaca'), ('jaltenco', 'Jaltenco'), ('jilotepec', 'Jilotepec'),
                    ('jilotzingo', 'Jilotzingo'), ('jiquipilco', 'Jiquipilco'), ('jocotitlan', 'Jocotitlán'),
                    ('joquicingo', 'Joquicingo'), ('juchitepec', 'Juchitepec'), ('la_paz', 'La Paz'),
                    ('lerma', 'Lerma'), ('luvianos', 'Luvianos'), ('malinalco', 'Malinalco'),
                    ('melchor_ocampo', 'Melchor Ocampo'), ('metepec', 'Metepec'), ('mexicaltzingo', 'Mexicaltzingo'),
                    ('morelos', 'Morelos'), ('naucalpan_de_juarez', 'Naucalpan de Juárez'),
                    ('nezahualcoyotl', 'Nezahualcóyotl'), ('nextlalpan', 'Nextlalpan'),
                    ('nicolas_romero', 'Nicolás Romero'), ('nopaltepec', 'Nopaltepec'), ('ocoyoacac', 'Ocoyoacac'),
                    ('ocuilan', 'Ocuilan'), ('otumba', 'Otumba'), ('otzoloapan', 'Otzoloapan'),
                    ('otzolotepec', 'Otzolotepec'), ('ozumba', 'Ozumba'), ('papalotla', 'Papalotla'),
                    ('polotitlan', 'Polotitlán'), ('rayon', 'Rayón'), ('san_antonio_la_isla', 'San Antonio la Isla'),
                    ('san_felipe_del_progreso', 'San Felipe del Progreso'),
                    ('san_martin_de_las_piramides', 'San Martín de las Pirámides'),
                    ('san_mateo_atenco', 'San Mateo Atenco'), ('san_simon_de_guerrero', 'San Simón de Guerrero'),
                    ('santo_tomas', 'Santo Tomás'), ('soyaniquilpan_de_juarez', 'Soyaniquilpan de Juárez'),
                    ('sultepec', 'Sultepec'), ('tecamac', 'Tecámac'), ('tejupilco', 'Tejupilco'),
                    ('temamatla', 'Temamatla'), ('temascalapa', 'Temascalapa'), ('temascalcingo', 'Temascalcingo'),
                    ('temascaltepec', 'Temascaltepec'), ('temoaya', 'Temoaya'), ('tenancingo', 'Tenancingo'),
                    ('tenango_del_aire', 'Tenango del Aire'), ('tenango_del_valle', 'Tenango del Valle'),
                    ('teoloyucan', 'Teoloyucan'), ('teotihuacan', 'Teotihuacán'), ('tepetlaoxtoc', 'Tepetlaoxtoc'),
                    ('tepetlixpa', 'Tepetlixpa'), ('tepotzotlan', 'Tepotzotlán'), ('tequixquiac', 'Tequixquiac'),
                    ('texcaltitlan', 'Texcaltitlán'), ('texcalyacac', 'Texcalyacac'), ('texcoco', 'Texcoco'),
                    ('tezoyuca', 'Tezoyuca'), ('tianguistenco', 'Tianguistenco'), ('timilpan', 'Timilpan'),
                    ('tlalmanalco', 'Tlalmanalco'), ('tlalnepantla_de_baz', 'Tlalnepantla de Baz'),
                    ('tlatlaya', 'Tlatlaya'), ('toluca', 'Toluca'), ('tonanitla', 'Tonanitla'),
                    ('tonatico', 'Tonatico'),
                    ('tultepec', 'Tultepec'), ('tultitlan', 'Tultitlán'), ('valle_de_bravo', 'Valle de Bravo'),
                    ('valle_de_chalco_solidaridad', 'Valle de Chalco Solidaridad'),
                    ('villa_de_allende', 'Villa de Allende'),
                    ('villa_del_carbon', 'Villa del Carbón'), ('villa_guerrero', 'Villa Guerrero'),
                    ('villa_victoria', 'Villa Victoria'), ('xonacatlan', 'Xonacatlán'), ('zacazonapan', 'Zacazonapan'),
                    ('zacualpan', 'Zacualpan'), ('zinacantepec', 'Zinacantepec'), ('zumpahuacan', 'Zumpahuacán'),
                    ('zumpango', 'Zumpango'),
                ],
                max_length=50,
                null=True,
                verbose_name='Municipio',
            ),
        ),

        # Eliminar los campos antiguos de ciudad y estado
        migrations.RemoveField(
            model_name='interesado',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='interesado',
            name='estado',
        ),
    ]
from django.db import models

# Create your models here.
# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define una clase gestora de usuario para crear usuarios con email."""

    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario con el email y contraseña dados."""
        if not email:
            raise ValueError('Los usuarios deben tener una dirección de email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario con el email y contraseña dados."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'administrador')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """Modelo de usuario personalizado que utiliza email como nombre de usuario."""

    ROLES = (
        ('interesado', 'Interesado'),
        ('reclutador', 'Reclutador'),
        ('administrador', 'Administrador'),
    )

    username = None
    email = models.EmailField(_('email'), unique=True)
    rol = models.CharField(max_length=15, choices=ROLES, default='interesado')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Interesado(models.Model):
    """Modelo para el perfil de un interesado/candidato."""

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='interesado')
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='interesados/', blank=True, null=True)

    def __str__(self):
        apellido_completo = f"{self.apellido_paterno} {self.apellido_materno}" if self.apellido_materno else self.apellido_paterno
        return f"{self.nombre} {apellido_completo}"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo con apellidos."""
        apellido_completo = f"{self.apellido_paterno} {self.apellido_materno}" if self.apellido_materno else self.apellido_paterno
        return f"{self.nombre} {apellido_completo}"


class Secretaria(models.Model):
    """Modelo para las secretarías (organizaciones) que pueden publicar vacantes."""

    nombre = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='secretarias/', blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    TAMAÑOS = (
        ('pequeña', 'Pequeña (1-50 empleados)'),
        ('mediana', 'Mediana (51-250 empleados)'),
        ('grande', 'Grande (251+ empleados)'),
    )
    tamaño = models.CharField(max_length=10, choices=TAMAÑOS, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Secretaría"
        verbose_name_plural = "Secretarías"


class Reclutador(models.Model):
    """Modelo para el perfil de un reclutador."""

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='reclutador')
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, related_name='reclutadores')
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        apellido_completo = f"{self.apellido_paterno} {self.apellido_materno}" if self.apellido_materno else self.apellido_paterno
        return f"{self.nombre} {apellido_completo} ({self.secretaria.nombre})"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo con apellidos."""
        apellido_completo = f"{self.apellido_paterno} {self.apellido_materno}" if self.apellido_materno else self.apellido_paterno
        return f"{self.nombre} {apellido_completo}"


#Agregar estos modelos al archivo existente

class Categoria(models.Model):
    """Modelo para las categorías de trabajo."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Vacante(models.Model):
    """Modelo para las vacantes de trabajo."""

    TIPOS_EMPLEO = (
        ('tiempo_completo', 'Tiempo Completo'),
        ('medio_tiempo', 'Medio Tiempo'),
        ('proyecto', 'Por Proyecto'),
        ('temporal', 'Temporal'),
        ('practicas', 'Prácticas Profesionales'),
    )

    MODALIDAD = (
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    )

    ESTADOS_VACANTE = (
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
        ('cerrada', 'Cerrada'),
        ('eliminada', 'Eliminada'),
    )

    ESTADOS_MEXICO = (
        ('aguascalientes', 'Aguascalientes'),
        ('baja_california', 'Baja California'),
        ('baja_california_sur', 'Baja California Sur'),
        ('campeche', 'Campeche'),
        ('chiapas', 'Chiapas'),
        ('chihuahua', 'Chihuahua'),
        ('ciudad_de_mexico', 'Ciudad de México'),
        ('coahuila', 'Coahuila'),
        ('colima', 'Colima'),
        ('durango', 'Durango'),
        ('estado_de_mexico', 'Estado de México'),
        ('guanajuato', 'Guanajuato'),
        ('guerrero', 'Guerrero'),
        ('hidalgo', 'Hidalgo'),
        ('jalisco', 'Jalisco'),
        ('michoacan', 'Michoacán'),
        ('morelos', 'Morelos'),
        ('nayarit', 'Nayarit'),
        ('nuevo_leon', 'Nuevo León'),
        ('oaxaca', 'Oaxaca'),
        ('puebla', 'Puebla'),
        ('queretaro', 'Querétaro'),
        ('quintana_roo', 'Quintana Roo'),
        ('san_luis_potosi', 'San Luis Potosí'),
        ('sinaloa', 'Sinaloa'),
        ('sonora', 'Sonora'),
        ('tabasco', 'Tabasco'),
        ('tamaulipas', 'Tamaulipas'),
        ('tlaxcala', 'Tlaxcala'),
        ('veracruz', 'Veracruz'),
        ('yucatan', 'Yucatán'),
        ('zacatecas', 'Zacatecas'),
    )

    # Información básica
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, related_name='vacantes')
    reclutador = models.ForeignKey(Reclutador, on_delete=models.CASCADE, related_name='vacantes')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='vacantes')

    # Condiciones de trabajo
    tipo_empleo = models.CharField(max_length=20, choices=TIPOS_EMPLEO)
    modalidad = models.CharField(max_length=15, choices=MODALIDAD, default='presencial')

    # Ubicación
    estado = models.CharField(max_length=30, choices=ESTADOS_MEXICO)
    ciudad = models.CharField(max_length=100)

    # Salario
    salario_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salario_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    detalles_salario = models.CharField(max_length=200, blank=True, null=True,
                                        help_text="Ej: A tratar, Según aptitudes, Más bonos")

    # Fechas
    fecha_inicio_estimada = models.DateField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Control de estado
    estado_vacante = models.CharField(max_length=15, choices=ESTADOS_VACANTE, default='borrador')
    aprobada = models.BooleanField(default=False)
    destacada = models.BooleanField(default=False)

    # Límites de postulación
    max_postulantes = models.IntegerField(choices=[(5, '5'), (10, '10'), (20, '20'), (50, '50')], default=20)
    max_postulaciones_por_interesado = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.titulo} - {self.secretaria.nombre}"

    @property
    def es_borrador(self):
        return self.estado_vacante == 'borrador'

    @property
    def es_publicada(self):
        return self.estado_vacante == 'publicada'

    @property
    def salario_formateado(self):
        """Retorna el salario formateado para mostrar."""
        if self.salario_min and self.salario_max:
            return f"${self.salario_min:,.0f} - ${self.salario_max:,.0f} MXN"
        elif self.salario_min:
            return f"Desde ${self.salario_min:,.0f} MXN"
        elif self.salario_max:
            return f"Hasta ${self.salario_max:,.0f} MXN"
        elif self.detalles_salario:
            return self.detalles_salario
        else:
            return "No especificado"

    class Meta:
        verbose_name = "Vacante"
        verbose_name_plural = "Vacantes"
        ordering = ['-fecha_publicacion']


class RequisitoVacante(models.Model):
    """Modelo para los requisitos específicos de una vacante."""

    vacante = models.OneToOneField(Vacante, on_delete=models.CASCADE, related_name='requisitos')
    educacion_minima = models.CharField(max_length=200, blank=True, null=True)
    experiencia_minima = models.CharField(max_length=200, blank=True, null=True)
    descripcion_requisitos = models.TextField(
        help_text="Detalla los requisitos específicos, habilidades técnicas, etc."
    )

    def __str__(self):
        return f"Requisitos - {self.vacante.titulo}"

    class Meta:
        verbose_name = "Requisito de Vacante"
        verbose_name_plural = "Requisitos de Vacantes"
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
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='interesados/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


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
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.secretaria.nombre})"
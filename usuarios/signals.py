# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import Interesado, Reclutador

Usuario = get_user_model()

@receiver(post_save, sender=Usuario)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea el perfil correspondiente cuando se crea un usuario."""
    if created:
        if instance.rol == 'interesado' and not hasattr(instance, 'interesado'):
            Interesado.objects.create(
                usuario=instance,
                nombre='',
                apellido_paterno='',
                apellido_materno=''
            )
        # Los perfiles de reclutador se crean manualmente durante el registro
        # porque necesitan asociarse a una secretaría

@receiver(post_save, sender=Reclutador)
def notificar_nueva_solicitud_reclutador(sender, instance, created, **kwargs):
    """Notifica a los administradores cuando se registra un nuevo reclutador."""
    if created:
        # Enviar correo electrónico a administradores (en producción)
        # Este es solo un ejemplo, ajustarlo según configuración de correo
        try:
            subject = 'Nueva solicitud de reclutador'
            message = f'Se ha registrado un nuevo reclutador: {instance.nombre_completo} de {instance.secretaria.nombre}.'
            from_email = settings.DEFAULT_FROM_EMAIL
            # Obtener lista de emails de administradores
            admin_emails = [u.email for u in Usuario.objects.filter(is_staff=True)]
            if admin_emails:
                send_mail(subject, message, from_email, admin_emails, fail_silently=True)
        except Exception as e:
            # Log error, no interrumpir el flujo
            print(f"Error enviando notificación: {e}")
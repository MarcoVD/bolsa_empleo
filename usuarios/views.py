# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db import transaction
from .forms import VacanteForm, RequisitoVacanteForm
from .models import Vacante, RequisitoVacante
from .forms import (
    LoginForm, InteresadoRegistroForm,
    SecretariaRegistroForm, ReclutadorRegistroForm
)
from .models import Usuario, Interesado, Reclutador, Secretaria

# usuarios/views.py - Agregar estas vistas al archivo existente
@method_decorator(login_required, name='dispatch')
class PublicarVacanteView(View):
    """Vista para publicar una nueva vacante."""

    def get(self, request):
        if request.user.rol != 'reclutador':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        if not hasattr(request.user, 'reclutador') or not request.user.reclutador.aprobado:
            messages.error(request, 'Tu cuenta de reclutador debe estar aprobada para publicar vacantes.')
            return redirect('dashboard_reclutador')

        vacante_form = VacanteForm()
        requisito_form = RequisitoVacanteForm()

        context = {
            'vacante_form': vacante_form,
            'requisito_form': requisito_form,
            'accion': 'crear'
        }
        return render(request, 'usuarios/publicar_vacante.html', context)

    def post(self, request):
        if request.user.rol != 'reclutador':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        if not hasattr(request.user, 'reclutador') or not request.user.reclutador.aprobado:
            messages.error(request, 'Tu cuenta de reclutador debe estar aprobada para publicar vacantes.')
            return redirect('dashboard_reclutador')

        reclutador = request.user.reclutador
        vacante_form = VacanteForm(request.POST)
        requisito_form = RequisitoVacanteForm(request.POST)

        if vacante_form.is_valid() and requisito_form.is_valid():
            try:
                with transaction.atomic():
                    # Determinar la acción del usuario
                    accion = request.POST.get('accion')

                    # Crear la vacante
                    vacante = vacante_form.save(commit=False)
                    vacante.secretaria = reclutador.secretaria
                    vacante.reclutador = reclutador

                    # Establecer el estado según la acción
                    if accion == 'guardar_borrador':
                        vacante.estado_vacante = 'borrador'
                        mensaje = 'Vacante guardada como borrador exitosamente.'
                    elif accion == 'publicar':
                        vacante.estado_vacante = 'publicada'
                        vacante.aprobada = True  # Puedes cambiar esto si requieres aprobación admin
                        mensaje = 'Vacante publicada exitosamente.'
                    else:
                        vacante.estado_vacante = 'borrador'
                        mensaje = 'Vacante guardada como borrador exitosamente.'

                    vacante.save()

                    # Crear los requisitos
                    requisito = requisito_form.save(commit=False)
                    requisito.vacante = vacante
                    requisito.save()

                    messages.success(request, mensaje)
                    return redirect('mis_vacantes')

            except Exception as e:
                messages.error(request, f'Error al guardar la vacante: {str(e)}')

        context = {
            'vacante_form': vacante_form,
            'requisito_form': requisito_form,
            'accion': 'crear'
        }
        return render(request, 'usuarios/publicar_vacante.html', context)


@method_decorator(login_required, name='dispatch')
class EditarVacanteView(View):
    """Vista para editar una vacante existente."""

    def get(self, request, vacante_id):
        if request.user.rol != 'reclutador':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        try:
            vacante = Vacante.objects.get(
                id=vacante_id,
                reclutador=request.user.reclutador
            )
        except Vacante.DoesNotExist:
            messages.error(request, 'Vacante no encontrada o no tienes permiso para editarla.')
            return redirect('mis_vacantes')

        # Obtener o crear requisitos si no existen
        requisito, created = RequisitoVacante.objects.get_or_create(
            vacante=vacante,
            defaults={'descripcion_requisitos': ''}
        )

        vacante_form = VacanteForm(instance=vacante)
        requisito_form = RequisitoVacanteForm(instance=requisito)

        context = {
            'vacante_form': vacante_form,
            'requisito_form': requisito_form,
            'vacante': vacante,
            'accion': 'editar'
        }
        return render(request, 'usuarios/publicar_vacante.html', context)

    def post(self, request, vacante_id):
        if request.user.rol != 'reclutador':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        try:
            vacante = Vacante.objects.get(
                id=vacante_id,
                reclutador=request.user.reclutador
            )
        except Vacante.DoesNotExist:
            messages.error(request, 'Vacante no encontrada o no tienes permiso para editarla.')
            return redirect('mis_vacantes')

        # Obtener o crear requisitos si no existen
        requisito, created = RequisitoVacante.objects.get_or_create(
            vacante=vacante,
            defaults={'descripcion_requisitos': ''}
        )

        vacante_form = VacanteForm(request.POST, instance=vacante)
        requisito_form = RequisitoVacanteForm(request.POST, instance=requisito)

        if vacante_form.is_valid() and requisito_form.is_valid():
            try:
                with transaction.atomic():
                    # Determinar la acción del usuario
                    accion = request.POST.get('accion')

                    # Actualizar la vacante
                    vacante = vacante_form.save(commit=False)

                    # Establecer el estado según la acción
                    if accion == 'guardar_borrador':
                        vacante.estado_vacante = 'borrador'
                        mensaje = 'Vacante actualizada y guardada como borrador.'
                    elif accion == 'publicar':
                        vacante.estado_vacante = 'publicada'
                        vacante.aprobada = True  # Puedes cambiar esto si requieres aprobación admin
                        mensaje = 'Vacante actualizada y publicada exitosamente.'
                    else:
                        mensaje = 'Vacante actualizada exitosamente.'

                    vacante.save()

                    # Actualizar los requisitos
                    requisito_form.save()

                    messages.success(request, mensaje)
                    return redirect('mis_vacantes')

            except Exception as e:
                messages.error(request, f'Error al actualizar la vacante: {str(e)}')

        context = {
            'vacante_form': vacante_form,
            'requisito_form': requisito_form,
            'vacante': vacante,
            'accion': 'editar'
        }
        return render(request, 'usuarios/publicar_vacante.html', context)


@method_decorator(login_required, name='dispatch')
class MisVacantesView(View):
    """Vista para listar las vacantes del reclutador."""

    def get(self, request):
        if request.user.rol != 'reclutador':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        vacantes = Vacante.objects.filter(
            reclutador=request.user.reclutador
        ).order_by('-fecha_actualizacion')

        context = {
            'vacantes': vacantes
        }
        return render(request, 'usuarios/mis_vacantes.html', context)

def index_view(request):
    """Vista de la página de inicio."""
    return render(request, 'usuarios/index.html')


class LoginView(View):
    """Vista para inicio de sesión de usuarios."""

    def get(self, request):
        form = LoginForm()
        return render(request, 'usuarios/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirigir según el rol
                if user.rol == 'interesado':
                    return redirect('perfil_interesado')
                elif user.rol == 'reclutador':
                    # Verificar si el reclutador está aprobado
                    if hasattr(user, 'reclutador') and user.reclutador.aprobado:
                        return redirect('dashboard_reclutador')
                    else:
                        messages.warning(request, 'Tu cuenta de reclutador está pendiente de aprobación.')
                        logout(request)
                        return redirect('login')
                elif user.rol == 'administrador':
                    return redirect('admin:index')
            else:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
        return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    return redirect('index')


class InteresadoRegistroView(View):
    """Vista para registro de interesados."""

    def get(self, request):
        form = InteresadoRegistroForm()
        return render(request, 'usuarios/registro_interesado.html', {'form': form})

    def post(self, request):
        form = InteresadoRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        return render(request, 'usuarios/registro_interesado.html', {'form': form})


class ReclutadorRegistroView(View):
    """Vista para registro de reclutadores."""

    def get(self, request):
        secretaria_form = SecretariaRegistroForm()
        reclutador_form = ReclutadorRegistroForm()
        return render(request, 'usuarios/registro_reclutador.html', {
            'secretaria_form': secretaria_form,
            'reclutador_form': reclutador_form
        })

    def post(self, request):
        secretaria_form = SecretariaRegistroForm(request.POST)
        reclutador_form = ReclutadorRegistroForm(request.POST)

        if secretaria_form.is_valid() and reclutador_form.is_valid():
            secretaria = secretaria_form.save()
            user = reclutador_form.save(commit=True, secretaria=secretaria)
            messages.success(
                request,
                'Registro exitoso. Tu cuenta será revisada por un administrador. Te notificaremos por email cuando sea aprobada.'
            )
            return redirect('login')

        return render(request, 'usuarios/registro_reclutador.html', {
            'secretaria_form': secretaria_form,
            'reclutador_form': reclutador_form
        })


@method_decorator(login_required, name='dispatch')
class PerfilInteresadoView(View):
    """Vista para ver/editar perfil del interesado."""

    def get(self, request):
        if request.user.rol != 'interesado':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        interesado = request.user.interesado
        context = {
            'interesado': interesado
        }
        return render(request, 'usuarios/perfil_interesado.html', context)


@method_decorator(login_required, name='dispatch')
class DashboardReclutadorView(View):
    """Vista para dashboard del reclutador."""

    def get(self, request):
        if request.user.rol != 'reclutador':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        reclutador = request.user.reclutador

        # Calcular estadísticas de vacantes
        vacantes_activas = reclutador.vacantes.filter(estado_vacante='publicada').count()
        vacantes_borradores = reclutador.vacantes.filter(estado_vacante='borrador').count()
        vacantes_cerradas = reclutador.vacantes.filter(estado_vacante='cerrada').count()
        total_vacantes = reclutador.vacantes.count()

        # Obtener las últimas 3 vacantes para mostrar en el dashboard
        ultimas_vacantes = reclutador.vacantes.all().order_by('-fecha_actualizacion')[:3]

        # TODO: Cuando implementemos postulaciones, calcular estas estadísticas
        postulaciones_recibidas = 0  # Placeholder
        postulaciones_nuevas = 0  # Placeholder

        context = {
            'reclutador': reclutador,
            'vacantes_activas': vacantes_activas,
            'vacantes_borradores': vacantes_borradores,
            'vacantes_cerradas': vacantes_cerradas,
            'total_vacantes': total_vacantes,
            'ultimas_vacantes': ultimas_vacantes,
            'postulaciones_recibidas': postulaciones_recibidas,
            'postulaciones_nuevas': postulaciones_nuevas,
        }
        # return render(request, 'usuarios/dashboard_reclutador.html', context)'usuarios/dashboard_reclutador.html', context)

        return render(request, 'usuarios/dashboard_reclutador.html', context)
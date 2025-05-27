# from .models import Usuario, Interesado, Reclutador, Secretaria
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db import transaction
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout

from .models import (
    Usuario, Interesado, Reclutador, Secretaria, # Añadido por si se usan directamente en vistas
    Curriculum, ExperienciaLaboral, Educacion,
    HabilidadInteresado, IdiomaInteresado, Habilidad,
    Vacante, RequisitoVacante, Categoria # Añadido por si se usan directamente
)
from .forms import (
    LoginForm,  # <--- Importación añadida
    InteresadoRegistroForm, # Añadido para la vista de registro de interesados
    SecretariaRegistroForm, # Añadido para la vista de registro de reclutadores
    ReclutadorRegistroForm, # Añadido para la vista de registro de reclutadores
    VacanteForm,            # Añadido para las vistas de publicar/editar vacante
    RequisitoVacanteForm,   # Añadido para las vistas de publicar/editar vacante
    CurriculumForm,
    InteresadoPerfilForm,
    ExperienciaLaboralForm,
    EducacionForm,
    HabilidadInteresadoForm,
    IdiomaInteresadoForm
)
class LoginView(View):
    def get(self, request):
        form = LoginForm()  # Ahora LoginForm estará definido
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST) # Y aquí también
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}!')
                # Redirigir según el tipo de usuario
                if hasattr(user, 'empresa'):
                    return redirect('usuarios:dashboard_empresa')
                elif hasattr(user, 'postulante'):
                    return redirect('usuarios:dashboard_postulante')
                else:
                    # Manejar caso de superusuario u otro tipo de usuario sin perfil específico
                    return redirect('pagina_principal') # O alguna vista por defecto
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            # Si el formulario no es válido, mostrar errores
            # (Django renderizará los errores automáticamente en la plantilla si usas {{ form.errors }})
            messages.error(request, 'Por favor corrige los errores en el formulario.')
        return render(request, 'login.html', {'form': form})
@method_decorator(login_required, name='dispatch')
class CrearEditarCVView(View):
    """Vista para crear o editar el CV del interesado."""

    def get(self, request):
        if request.user.rol != 'interesado':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        interesado = request.user.interesado

        # Obtener o crear curriculum
        curriculum, created = Curriculum.objects.get_or_create(
            interesado=interesado,
            defaults={'resumen_profesional': ''}
        )

        # Preparar formularios
        curriculum_form = CurriculumForm(instance=curriculum)
        perfil_form = InteresadoPerfilForm(instance=interesado)

        # Obtener experiencias, educación, habilidades e idiomas existentes
        experiencias = curriculum.experiencias.all()
        educaciones = curriculum.educaciones.all()
        habilidades = curriculum.habilidades.all()
        idiomas = curriculum.idiomas.all()

        context = {
            'curriculum': curriculum,
            'curriculum_form': curriculum_form,
            'perfil_form': perfil_form,
            'experiencias': experiencias,
            'educaciones': educaciones,
            'habilidades': habilidades,
            'idiomas': idiomas,
            'es_nuevo': created,
        }
        return render(request, 'usuarios/crear_editar_cv.html', context)

    def post(self, request):
        if request.user.rol != 'interesado':
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('index')

        interesado = request.user.interesado
        curriculum, created = Curriculum.objects.get_or_create(
            interesado=interesado,
            defaults={'resumen_profesional': ''}
        )

        curriculum_form = CurriculumForm(request.POST, instance=curriculum)
        perfil_form = InteresadoPerfilForm(request.POST, instance=interesado)

        if curriculum_form.is_valid() and perfil_form.is_valid():
            try:
                with transaction.atomic():
                    perfil_form.save()
                    curriculum_form.save()
                    messages.success(request, 'CV actualizado exitosamente.')
                    return redirect('crear_editar_cv')
            except Exception as e:
                messages.error(request, f'Error al guardar el CV: {str(e)}')

        # Si hay errores, volver a mostrar el formulario
        experiencias = curriculum.experiencias.all()
        educaciones = curriculum.educaciones.all()
        habilidades = curriculum.habilidades.all()
        idiomas = curriculum.idiomas.all()

        context = {
            'curriculum': curriculum,
            'curriculum_form': curriculum_form,
            'perfil_form': perfil_form,
            'experiencias': experiencias,
            'educaciones': educaciones,
            'habilidades': habilidades,
            'idiomas': idiomas,
            'es_nuevo': created,
        }
        return render(request, 'usuarios/crear_editar_cv.html', context)


@login_required
def editar_experiencia_ajax(request, experiencia_id):
    """Vista AJAX para editar experiencia laboral."""
    if request.method != 'POST' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id, curriculum=curriculum)

        # Usar la instancia existente para editar
        form = ExperienciaLaboralForm(request.POST, instance=experiencia)

        if form.is_valid():
            experiencia_actualizada = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Experiencia actualizada exitosamente',
                'experiencia': {
                    'id': experiencia_actualizada.id,
                    'empresa': experiencia_actualizada.empresa,
                    'puesto': experiencia_actualizada.puesto,
                    'periodo': experiencia_actualizada.periodo_trabajo
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def agregar_experiencia_ajax(request):
    """Vista AJAX para agregar experiencia laboral."""
    if request.method != 'POST' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        form = ExperienciaLaboralForm(request.POST)

        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.curriculum = curriculum
            experiencia.save()

            return JsonResponse({
                'success': True,
                'message': 'Experiencia agregada exitosamente',
                'experiencia': {
                    'id': experiencia.id,
                    'empresa': experiencia.empresa,
                    'puesto': experiencia.puesto,
                    'periodo': experiencia.periodo_trabajo
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def agregar_educacion_ajax(request):
    """Vista AJAX para agregar educación."""
    if request.method != 'POST' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        form = EducacionForm(request.POST)

        if form.is_valid():
            educacion = form.save(commit=False)
            educacion.curriculum = curriculum
            educacion.save()

            return JsonResponse({
                'success': True,
                'message': 'Educación agregada exitosamente',
                'educacion': {
                    'id': educacion.id,
                    'titulo': educacion.titulo,
                    'institucion': educacion.institucion,
                    'periodo': educacion.periodo_estudio
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def agregar_habilidad_ajax(request):
    """Vista AJAX para agregar habilidad."""
    if request.method != 'POST' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        nombre_habilidad = request.POST.get('nombre_habilidad')
        nivel = request.POST.get('nivel')

        if not nombre_habilidad or not nivel:
            return JsonResponse({
                'success': False,
                'error': 'Nombre de habilidad y nivel son requeridos'
            })

        # Obtener o crear la habilidad
        habilidad, created = Habilidad.objects.get_or_create(
            nombre=nombre_habilidad,
            defaults={'descripcion': ''}
        )

        # Crear o actualizar la relación
        habilidad_interesado, created = HabilidadInteresado.objects.get_or_create(
            curriculum=curriculum,
            habilidad=habilidad,
            defaults={'nivel': nivel}
        )

        if not created:
            habilidad_interesado.nivel = nivel
            habilidad_interesado.save()

        return JsonResponse({
            'success': True,
            'message': 'Habilidad agregada exitosamente',
            'habilidad': {
                'id': habilidad_interesado.id,
                'nombre': habilidad.nombre,
                'nivel': habilidad_interesado.get_nivel_display()
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def agregar_idioma_ajax(request):
    """Vista AJAX para agregar idioma."""
    if request.method != 'POST' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        form = IdiomaInteresadoForm(request.POST)

        if form.is_valid():
            idioma = form.save(commit=False)
            idioma.curriculum = curriculum
            idioma.save()

            return JsonResponse({
                'success': True,
                'message': 'Idioma agregado exitosamente',
                'idioma': {
                    'id': idioma.id,
                    'idioma': idioma.idioma,
                    'nivel_general': idioma.nivel_general
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def eliminar_experiencia_ajax(request, experiencia_id):
    """Vista AJAX para eliminar experiencia laboral."""
    if request.method != 'DELETE' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id, curriculum=curriculum)
        experiencia.delete()

        return JsonResponse({
            'success': True,
            'message': 'Experiencia eliminada exitosamente'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def eliminar_educacion_ajax(request, educacion_id):
    """Vista AJAX para eliminar educación."""
    if request.method != 'DELETE' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        educacion = get_object_or_404(Educacion, id=educacion_id, curriculum=curriculum)
        educacion.delete()

        return JsonResponse({
            'success': True,
            'message': 'Educación eliminada exitosamente'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def eliminar_habilidad_ajax(request, habilidad_id):
    """Vista AJAX para eliminar habilidad."""
    if request.method != 'DELETE' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        habilidad = get_object_or_404(HabilidadInteresado, id=habilidad_id, curriculum=curriculum)
        habilidad.delete()

        return JsonResponse({
            'success': True,
            'message': 'Habilidad eliminada exitosamente'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def eliminar_idioma_ajax(request, idioma_id):
    """Vista AJAX para eliminar idioma."""
    if request.method != 'DELETE' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        curriculum = request.user.interesado.curriculum
        idioma = get_object_or_404(IdiomaInteresado, id=idioma_id, curriculum=curriculum)
        idioma.delete()

        return JsonResponse({
            'success': True,
            'message': 'Idioma eliminado exitosamente'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def previsualizar_cv(request):
    """Vista para previsualizar el CV completo."""
    if request.user.rol != 'interesado':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('index')

    interesado = request.user.interesado

    try:
        curriculum = interesado.curriculum
        context = {
            'interesado': interesado,
            'curriculum': curriculum,
            'experiencias': curriculum.experiencias.all(),
            'educaciones': curriculum.educaciones.all(),
            'habilidades': curriculum.habilidades.all(),
            'idiomas': curriculum.idiomas.all(),
        }
        return render(request, 'usuarios/previsualizar_cv.html', context)
    except Curriculum.DoesNotExist:
        messages.warning(request, 'Primero debes crear tu CV.')
        return redirect('crear_editar_cv')


# usuarios/views.py
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
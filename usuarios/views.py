# from .models import Usuario, Interesado, Reclutador, Secretaria
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db import transaction
from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import render_to_string
# import weasyprint
from weasyprint import HTML
from io import BytesIO
from PIL import Image
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io
import os
import uuid


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
                messages.error(request, 'Correo o contraseña incorrectos. Intenta nuevamente.')
        return render(request, 'usuarios/login.html', {'form': form})

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


# usuarios/views.py - Vista actualizada para manejar guardado automático de imagen

@login_required
def actualizar_perfil_ajax(request):
    """Vista AJAX para actualizar perfil del interesado."""
    if request.method != 'POST' or request.user.rol != 'interesado':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        interesado = request.user.interesado

        # Verificar si solo se está actualizando la foto
        only_photo = 'foto_perfil' in request.FILES and len(request.POST) <= 2  # Solo CSRF y posiblemente un campo más

        if not only_photo:
            # Actualizar campos de texto solo si no es actualización de foto únicamente
            interesado.nombre = request.POST.get('nombre', interesado.nombre)
            interesado.apellido_paterno = request.POST.get('apellido_paterno', interesado.apellido_paterno)
            interesado.apellido_materno = request.POST.get('apellido_materno', interesado.apellido_materno)
            interesado.telefono = request.POST.get('telefono', interesado.telefono)
            interesado.municipio = request.POST.get('municipio', interesado.municipio)
            interesado.codigo_postal = request.POST.get('codigo_postal', interesado.codigo_postal)

            # Fecha de nacimiento
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            if fecha_nacimiento:
                interesado.fecha_nacimiento = fecha_nacimiento

        # Validar y procesar foto de perfil
        if 'foto_perfil' in request.FILES:
            foto = request.FILES['foto_perfil']

            # Validar tipo de archivo
            if not foto.name.lower().endswith(('.jpg', '.jpeg')):
                return JsonResponse({
                    'success': False,
                    'error': 'Solo se permiten archivos JPG'
                })

            # Validar tamaño (5MB máximo)
            if foto.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'El archivo es demasiado grande. Máximo 5MB'
                })

            # Para imágenes ya recortadas (blob), no necesitan procesamiento adicional
            # Ya vienen en el tamaño correcto de 160x160px
            interesado.foto_perfil = foto

        interesado.save()

        return JsonResponse({
            'success': True,
            'message': 'Perfil actualizado exitosamente' if not only_photo else 'Imagen guardada exitosamente',
            'data': {
                'nombre_completo': interesado.nombre_completo,
                'telefono': interesado.telefono or 'No especificado',
                'ubicacion': interesado.ubicacion_completa,
                'foto_url': interesado.foto_perfil.url if interesado.foto_perfil else None
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_http_methods(["POST"])
def actualizar_foto_perfil_ajax(request):
    """
    Vista AJAX específica para actualizar solo la foto de perfil del interesado
    """
    try:
        # Verificar que el usuario sea un interesado
        if not hasattr(request.user, 'interesado'):
            return JsonResponse({
                'success': False,
                'error': 'Usuario no autorizado'
            }, status=403)

        interesado = request.user.interesado

        # Verificar que se envió una foto
        if 'foto_perfil' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No se recibió ninguna imagen'
            }, status=400)

        foto_file = request.FILES['foto_perfil']

        # Validar tipo de archivo
        if not foto_file.content_type.startswith('image/'):
            return JsonResponse({
                'success': False,
                'error': 'El archivo debe ser una imagen'
            }, status=400)

        # Validar tamaño del archivo (5MB máximo)
        if foto_file.size > 5 * 1024 * 1024:  # 5MB
            return JsonResponse({
                'success': False,
                'error': 'La imagen no debe superar los 5MB'
            }, status=400)

        # Procesar la imagen
        try:
            # Abrir la imagen con PIL para procesarla
            image = Image.open(foto_file)

            # Convertir a RGB si es necesario (para JPEGs)
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')

            # Redimensionar si es muy grande (máximo 800x800 antes de guardar)
            max_size = (800, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Guardar la imagen procesada en memoria
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

            # Generar nombre único para el archivo
            filename = f"perfil_{interesado.id}_{uuid.uuid4().hex[:8]}.jpg"

            # Eliminar foto anterior si existe
            if interesado.foto_perfil:
                try:
                    # Eliminar archivo físico anterior
                    if default_storage.exists(interesado.foto_perfil.name):
                        default_storage.delete(interesado.foto_perfil.name)
                except Exception as e:
                    # Log el error pero continúa (no es crítico)
                    print(f"Error al eliminar foto anterior: {e}")

            # Guardar nueva foto
            foto_content = ContentFile(output.getvalue(), name=filename)
            interesado.foto_perfil.save(filename, foto_content, save=True)

            # Construir URL completa de la foto
            foto_url = request.build_absolute_uri(interesado.foto_perfil.url)

            return JsonResponse({
                'success': True,
                'message': 'Foto de perfil actualizada correctamente',
                'photo_url': foto_url,
                'photo_name': filename
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar la imagen: {str(e)}'
            }, status=500)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)


# Alternativa más simple si no quieres usar PIL
@login_required
@require_http_methods(["POST"])
def actualizar_foto_perfil_simple(request):
    """
    Versión simplificada sin procesamiento de imagen con PIL
    """
    try:
        if not hasattr(request.user, 'interesado'):
            return JsonResponse({
                'success': False,
                'error': 'Usuario no autorizado'
            }, status=403)

        interesado = request.user.interesado

        if 'foto_perfil' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No se recibió ninguna imagen'
            }, status=400)

        foto_file = request.FILES['foto_perfil']

        # Validaciones básicas
        if not foto_file.content_type.startswith('image/'):
            return JsonResponse({
                'success': False,
                'error': 'El archivo debe ser una imagen'
            }, status=400)

        if foto_file.size > 5 * 1024 * 1024:  # 5MB
            return JsonResponse({
                'success': False,
                'error': 'La imagen no debe superar los 5MB'
            }, status=400)

        # Eliminar foto anterior si existe
        if interesado.foto_perfil:
            try:
                if default_storage.exists(interesado.foto_perfil.name):
                    default_storage.delete(interesado.foto_perfil.name)
            except Exception:
                pass  # Continuar aunque falle la eliminación

        # Guardar nueva foto directamente
        interesado.foto_perfil = foto_file
        interesado.save()

        # Construir URL completa
        foto_url = request.build_absolute_uri(interesado.foto_perfil.url)

        return JsonResponse({
            'success': True,
            'message': 'Foto de perfil actualizada correctamente',
            'photo_url': foto_url
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al guardar la foto: {str(e)}'
        }, status=500)


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


def descargar_cv_pdf(request):
    """Vista para generar y descargar CV en PDF."""
    if request.user.rol != 'interesado':
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('index')

    interesado = request.user.interesado

    try:
        curriculum = interesado.curriculum
    except Curriculum.DoesNotExist:
        messages.warning(request, 'Primero debes crear tu CV.')
        return redirect('crear_editar_cv')

    # Preparar datos para el PDF
    context = {
        'interesado': interesado,
        'curriculum': curriculum,
        'experiencias': curriculum.experiencias.all(),
        'educaciones': curriculum.educaciones.all(),
        'habilidades': curriculum.habilidades.all(),
        'idiomas': curriculum.idiomas.all(),
    }

    # Renderizar HTML
    html_string = render_to_string('usuarios/cv_pdf_template.html', context)

    # Generar PDF
    try:
        html_doc = HTML(string=html_string)
        pdf_bytes = html_doc.write_pdf()

        # Preparar respuesta
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"CV_{interesado.nombre}_{interesado.apellido_paterno}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
    except Exception as e:
        messages.error(request, f'Error al generar PDF: {str(e)}')
        return redirect('perfil_interesado')


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
    """Vista de la página de inicio con vacantes publicadas."""
    # Obtener solo las vacantes publicadas y aprobadas
    vacantes = Vacante.objects.filter(
        estado_vacante='publicada',
        aprobada=True
    ).select_related('secretaria', 'reclutador', 'categoria').order_by('-fecha_publicacion')[:12]

    # Contar total de vacantes para mostrar estadística
    total_vacantes = vacantes.count()

    context = {
        'vacantes': vacantes,
        'total_vacantes': total_vacantes,
    }
    return render(request, 'usuarios/index.html', context)



def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
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

        # Verificar si existe CV
        tiene_cv = hasattr(interesado, 'curriculum')

        context = {
            'interesado': interesado,
            'tiene_cv': tiene_cv
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

def detalle_vacante_view(request, vacante_id):
    """
    Muestra los detalles de una vacante específica.
    """
    vacante = get_object_or_404(
        Vacante.objects.select_related('secretaria', 'categoria', 'requisitos'),
        id=vacante_id,
        estado_vacante='publicada',
        aprobada=True
    )

    try:
        requisitos = vacante.requisitos
    except RequisitoVacante.DoesNotExist:
        requisitos = None
    except AttributeError:
        requisitos = None

    context = {
        'vacante': vacante,
        'requisitos': requisitos,
    }
    return render(request, 'usuarios/detalle_vacante.html', context)


# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/interesado/', views.InteresadoRegistroView.as_view(), name='registro_interesado'),
    path('registro/reclutador/', views.ReclutadorRegistroView.as_view(), name='registro_reclutador'),
    path('perfil/interesado/', views.PerfilInteresadoView.as_view(), name='perfil_interesado'),
    path('dashboard/reclutador/', views.DashboardReclutadorView.as_view(), name='dashboard_reclutador'),

    # URLs para vacantes
    path('publicar-vacante/', views.PublicarVacanteView.as_view(), name='publicar_vacante'),
    path('editar-vacante/<int:vacante_id>/', views.EditarVacanteView.as_view(), name='editar_vacante'),
    path('mis-vacantes/', views.MisVacantesView.as_view(), name='mis_vacantes'),
    # NUEVA URL PARA DETALLE DE VACANTE
    path('vacante/<int:vacante_id>/', views.detalle_vacante_view, name='detalle_vacante'),

    # URLs para CV
    path('mi-cv/', views.CrearEditarCVView.as_view(), name='crear_editar_cv'),
    path('mi-cv/previsualizar/', views.previsualizar_cv, name='previsualizar_cv'),
    path('ajax/actualizar-perfil/', views.actualizar_perfil_ajax, name='actualizar_perfil_ajax'),

    # URLs AJAX para CV (solo las que existen en views.py)
    path('ajax/experiencia/agregar/', views.agregar_experiencia_ajax, name='agregar_experiencia_ajax'),
    path('ajax/experiencia/editar/<int:experiencia_id>/', views.editar_experiencia_ajax,
         name='editar_experiencia_ajax'),
    path('ajax/experiencia/eliminar/<int:experiencia_id>/', views.eliminar_experiencia_ajax,
         name='eliminar_experiencia_ajax'),

    path('ajax/educacion/agregar/', views.agregar_educacion_ajax, name='agregar_educacion_ajax'),
    path('ajax/educacion/eliminar/<int:educacion_id>/', views.eliminar_educacion_ajax, name='eliminar_educacion_ajax'),

    path('ajax/habilidad/agregar/', views.agregar_habilidad_ajax, name='agregar_habilidad_ajax'),
    path('ajax/habilidad/eliminar/<int:habilidad_id>/', views.eliminar_habilidad_ajax, name='eliminar_habilidad_ajax'),

    path('ajax/idioma/agregar/', views.agregar_idioma_ajax, name='agregar_idioma_ajax'),
    path('ajax/idioma/eliminar/<int:idioma_id>/', views.eliminar_idioma_ajax, name='eliminar_idioma_ajax'),
]
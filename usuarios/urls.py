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
]
from django.shortcuts import render

# Create your views here.
# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View
from .forms import (
    LoginForm, InteresadoRegistroForm,
    SecretariaRegistroForm, ReclutadorRegistroForm
)
from .models import Usuario, Interesado, Reclutador, Secretaria


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
        context = {
            'reclutador': reclutador
        }
        return render(request, 'usuarios/dashboard_reclutador.html', context)
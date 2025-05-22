# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Interesado, Reclutador, Secretaria

Usuario = get_user_model()


class LoginForm(AuthenticationForm):
    """Formulario para inicio de sesión."""

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )


class InteresadoRegistroForm(UserCreationForm):
    """Formulario para registro de interesados."""

    nombre = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'})
    )
    apellido_paterno = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido paterno'})
    )
    apellido_materno = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido materno (opcional)'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'interesado'
        if commit:
            user.save()
            # Crear el perfil solo si no existe
            Interesado.objects.get_or_create(
                usuario=user,
                defaults={
                    'nombre': self.cleaned_data.get('nombre'),
                    'apellido_paterno': self.cleaned_data.get('apellido_paterno'),
                    'apellido_materno': self.cleaned_data.get('apellido_materno')
                }
            )
        return user


class SecretariaRegistroForm(forms.ModelForm):
    """Formulario para registro de secretarías."""

    class Meta:
        model = Secretaria
        fields = ('nombre', 'rfc', 'descripcion', 'sitio_web', 'direccion')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la secretaría'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC de la secretaría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción breve'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.example.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'})
        }


class ReclutadorRegistroForm(UserCreationForm):
    """Formulario para registro de reclutadores."""

    nombre = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'})
    )
    apellido_paterno = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido paterno'})
    )
    apellido_materno = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido materno (opcional)'})
    )
    cargo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su cargo'})
    )
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su teléfono'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True, secretaria=None):
        if not secretaria:
            raise ValueError("Se requiere una secretaría para el registro de reclutador")

        user = super().save(commit=False)
        user.rol = 'reclutador'
        if commit:
            user.save()
            Reclutador.objects.create(
                usuario=user,
                secretaria=secretaria,
                nombre=self.cleaned_data.get('nombre'),
                apellido_paterno=self.cleaned_data.get('apellido_paterno'),
                apellido_materno=self.cleaned_data.get('apellido_materno'),
                cargo=self.cleaned_data.get('cargo'),
                telefono=self.cleaned_data.get('telefono'),
                aprobado=False
            )
        return user
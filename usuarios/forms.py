# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Interesado, Reclutador, Secretaria, Vacante, RequisitoVacante
# from .models import Vacante, RequisitoVacante, Categoria
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

# usuarios/forms.py - Agregar estos formularios al archivo existente




class VacanteForm(forms.ModelForm):
    """Formulario para crear/editar vacantes."""

    class Meta:
        model = Vacante
        fields = [
            'titulo', 'categoria', 'tipo_empleo', 'descripcion',
            'estado', 'ciudad', 'salario_min', 'salario_max', 'detalles_salario',
            'fecha_inicio_estimada', 'fecha_limite', 'max_postulantes', 'modalidad'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Desarrollador Fullstack Senior'
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tipo_empleo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe las funciones, responsabilidades, el equipo de trabajo, la cultura de la empresa, etc.'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Guadalajara, Benito Juárez'
            }),
            'salario_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 20000',
                'min': '0'
            }),
            'salario_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 35000',
                'min': '0'
            }),
            'detalles_salario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: A tratar, Según aptitudes, Más bonos'
            }),
            'fecha_inicio_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_limite': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'max_postulantes': forms.Select(attrs={'class': 'form-select'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'titulo': 'Título de la Vacante',
            'categoria': 'Categoría de la Vacante',
            'tipo_empleo': 'Tipo de Empleo',
            'descripcion': 'Descripción Detallada de la Vacante',
            'estado': 'Estado',
            'ciudad': 'Municipio / Alcaldía',
            'salario_min': 'Salario Mínimo (MXN, opcional)',
            'salario_max': 'Salario Máximo (MXN, opcional)',
            'detalles_salario': 'Detalles Adicionales del Salario (opcional)',
            'fecha_inicio_estimada': 'Fecha Estimada de Inicio (opcional)',
            'fecha_limite': 'Fecha Límite de Postulación',
            'max_postulantes': 'Número Máximo de Postulantes',
            'modalidad': 'Modalidad de Trabajo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos obligatorios
        self.fields['titulo'].required = True
        self.fields['categoria'].required = True
        self.fields['tipo_empleo'].required = True
        self.fields['descripcion'].required = True
        self.fields['estado'].required = True
        self.fields['ciudad'].required = True
        self.fields['fecha_limite'].required = True
        self.fields['max_postulantes'].required = True

    def clean(self):
        cleaned_data = super().clean()
        salario_min = cleaned_data.get('salario_min')
        salario_max = cleaned_data.get('salario_max')

        # Validar que el salario mínimo no sea mayor al máximo
        if salario_min and salario_max:
            if salario_min > salario_max:
                raise forms.ValidationError(
                    "El salario mínimo no puede ser mayor al salario máximo."
                )

        # Validar que la fecha límite sea posterior a hoy
        fecha_limite = cleaned_data.get('fecha_limite')
        if fecha_limite:
            from datetime import date
            if fecha_limite <= date.today():
                raise forms.ValidationError(
                    "La fecha límite debe ser posterior a la fecha actual."
                )

        return cleaned_data


class RequisitoVacanteForm(forms.ModelForm):
    """Formulario para los requisitos de la vacante."""

    class Meta:
        model = RequisitoVacante
        fields = ['educacion_minima', 'experiencia_minima', 'descripcion_requisitos']
        widgets = {
            'educacion_minima': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Licenciatura en Informática (Titulado)'
            }),
            'experiencia_minima': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3+ años de experiencia en desarrollo web'
            }),
            'descripcion_requisitos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Ej: - Licenciatura en Informática (Titulado).\n- 3+ años de experiencia con Python/Django.\n- Conocimiento de bases de datos PostgreSQL.\n- Habilidades de comunicación efectiva.'
            }),
        }
        labels = {
            'educacion_minima': 'Educación Mínima (opcional)',
            'experiencia_minima': 'Experiencia Mínima (opcional)',
            'descripcion_requisitos': 'Requisitos (Educación, Experiencia, Habilidades)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion_requisitos'].required = True
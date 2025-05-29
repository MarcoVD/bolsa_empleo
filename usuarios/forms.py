# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .fields import CurrencyField
from .widgets import CurrencyInput
from .models import Interesado, Reclutador, Secretaria, Vacante, RequisitoVacante, Curriculum, ExperienciaLaboral, Educacion, HabilidadInteresado, IdiomaInteresado, Categoria
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
            # Crear el perfil de interesado con campos básicos vacíos
            Interesado.objects.get_or_create(
                usuario=user,
                defaults={
                    'nombre': '',
                    'apellido_paterno': '',
                    'apellido_materno': ''
                }
            )
        return user
# Formularios para CV

class CurriculumForm(forms.ModelForm):
    """Formulario para la información básica del CV."""

    class Meta:
        model = Curriculum
        fields = ['resumen_profesional']
        widgets = {
            'resumen_profesional': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ej: Profesional con 5 años de experiencia en desarrollo web...'
            })
        }

# usuarios/forms.py - FORMULARIO ACTUALIZADO PARA INTERESADO

class InteresadoPerfilForm(forms.ModelForm):
    """Formulario para editar la información personal del interesado."""

    class Meta:
        model = Interesado
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno', 'telefono',
            'fecha_nacimiento', 'direccion', 'municipio', 'codigo_postal'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su nombre'
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su apellido paterno'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su apellido materno (opcional)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 55 1234 5678'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Calle, Número, Colonia'
            }),
            'municipio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'C.P.'
            })
        }
        labels = {
            'nombre': 'Nombre(s)',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno (opcional)',
            'telefono': 'Teléfono',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Dirección',
            'municipio': 'Municipio del Estado de México',
            'codigo_postal': 'Código Postal'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar opción vacía al select de municipio
        municipio_choices = [('', 'Selecciona un municipio...')] + list(self.fields['municipio'].choices)
        self.fields['municipio'].choices = municipio_choices

class ExperienciaLaboralForm(forms.ModelForm):
    """Formulario para experiencias laborales."""

    class Meta:
        model = ExperienciaLaboral
        fields = ['empresa', 'puesto', 'descripcion', 'fecha_inicio', 'fecha_fin', 'actual']
        widgets = {
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tecnologías Acme S.A. de C.V.'
            }),
            'puesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Desarrollador Web'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe tus actividades principales...'
            }),
            # CAMBIAR ESTOS DOS WIDGETS:
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control date-picker',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control date-picker',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'actual': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'empresa': 'Empresa',
            'puesto': 'Puesto / Cargo',
            'descripcion': 'Funciones y Responsabilidades',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'actual': 'Trabajo actual'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar formato de fecha para input
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%d']


class EducacionForm(forms.ModelForm):
    """Formulario para educación."""

    class Meta:
        model = Educacion
        fields = ['titulo', 'institucion', 'fecha_inicio', 'fecha_fin', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ingeniería en Sistemas'
            }),
            'institucion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Universidad Nacional'
            }),
            # CAMBIAR ESTOS DOS WIDGETS:
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control date-picker',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control date-picker',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción adicional (opcional)'
            })
        }
        labels = {
            'titulo': 'Título Obtenido / Nivel',
            'institucion': 'Institución Educativa',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'descripcion': 'Descripción'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar formato de fecha para input
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%d']

class HabilidadInteresadoForm(forms.ModelForm):
    """Formulario para habilidades del interesado."""

    nombre_habilidad = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: JavaScript, Liderazgo'
        }),
        label='Habilidad'
    )

    class Meta:
        model = HabilidadInteresado
        fields = ['nivel']
        widgets = {
            'nivel': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'nivel': 'Nivel de Dominio'
        }


class IdiomaInteresadoForm(forms.ModelForm):
    """Formulario para idiomas del interesado."""

    class Meta:
        model = IdiomaInteresado
        fields = ['idioma', 'nivel_lectura', 'nivel_escritura', 'nivel_conversacion']
        widgets = {
            'idioma': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Inglés'
            }),
            'nivel_lectura': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nivel_escritura': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nivel_conversacion': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'idioma': 'Idioma',
            'nivel_lectura': 'Nivel de Lectura',
            'nivel_escritura': 'Nivel de Escritura',
            'nivel_conversacion': 'Nivel de Conversación'
        }


class SecretariaRegistroForm(forms.ModelForm):
    """Formulario para registro de secretarías."""

    class Meta:
        model = Secretaria
        fields = ('rfc', 'descripcion', 'sitio_web', 'direccion')  # Removido 'nombre'
        widgets = {
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC de la secretaría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción breve'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.example.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'})
        }

    def save(self, commit=True):
        secretaria = super().save(commit=False)
        # Forzar el nombre de la secretaría
        secretaria.nombre = 'Secretaría de Movilidad'
        if commit:
            secretaria.save()
        return secretaria
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

# usuarios/forms.py - SECCIÓN ACTUALIZADA PARA VACANTES

class VacanteForm(forms.ModelForm):
    """Formulario para crear/editar vacantes. Validar los campos las comas, espacios y numeros negativos """
    def clean_salario_min(self):
        valor = self.cleaned_data.get('salario_min')
        if valor:
            # Elimina comas y espacios
            valor_str = str(valor).replace(',', '').replace('$', '').strip()
            return float(valor_str)
        return valor

    def clean_salario_max(self):
        valor = self.cleaned_data.get('salario_max')
        if valor:
            valor_str = str(valor).replace(',', '').replace('$', '').strip()
            return float(valor_str)
        return valor

    class Meta:
        model = Vacante
        fields = [
            'titulo', 'categoria', 'tipo_empleo', 'descripcion',
            'municipio', 'salario_min', 'salario_max', 'detalles_salario',
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
            'municipio': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecciona un municipio...'
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
            'municipio': 'Municipio del Estado de México',
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
        self.fields['municipio'].required = True
        self.fields['fecha_limite'].required = True
        self.fields['max_postulantes'].required = True

        # Configurar ayuda para campos de salario
        self.fields['salario_min'].help_text = 'Ingresa el salario mínimo. Ejemplo: 25000.00 o 25,000.00'
        self.fields['salario_max'].help_text = 'Ingresa el salario máximo. Ejemplo: 35000.00 o 35,000.00'

        # Agregar opción vacía al select de municipio
        municipio_choices = [('', 'Selecciona un municipio...')] + list(self.fields['municipio'].choices)
        self.fields['municipio'].choices = municipio_choices

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
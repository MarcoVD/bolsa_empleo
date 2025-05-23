# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Interesado, Reclutador, Secretaria, Categoria, Vacante, RequisitoVacante


class InteresadoInline(admin.StackedInline):
    model = Interesado
    can_delete = False
    verbose_name_plural = 'Información de Interesado'


class ReclutadorInline(admin.StackedInline):
    model = Reclutador
    can_delete = False
    verbose_name_plural = 'Información de Reclutador'


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Extras'), {'fields': ('rol', 'activo')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'rol'),
            },
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'rol', 'is_staff', 'activo')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.rol == 'interesado':
                return [InteresadoInline]
            elif obj.rol == 'reclutador':
                return [ReclutadorInline]
        return []


@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rfc', 'ciudad', 'activa', 'fecha_registro')
    list_filter = ('activa', 'ciudad', 'estado')
    search_fields = ('nombre', 'rfc')
    date_hierarchy = 'fecha_registro'


@admin.register(Interesado)
class InteresadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'usuario', 'telefono')
    list_filter = ('ciudad', 'estado')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'usuario__email')


@admin.register(Reclutador)
class ReclutadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'secretaria', 'cargo', 'aprobado')
    list_filter = ('aprobado', 'secretaria')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'usuario__email', 'secretaria__nombre')
    list_editable = ('aprobado',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


class RequisitoVacanteInline(admin.StackedInline):
    model = RequisitoVacante
    can_delete = False
    verbose_name_plural = 'Requisitos de la Vacante'


@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'secretaria', 'reclutador', 'categoria',
        'estado_vacante', 'tipo_empleo', 'fecha_publicacion', 'fecha_limite'
    )
    list_filter = (
        'estado_vacante', 'tipo_empleo', 'modalidad', 'categoria',
        'secretaria', 'aprobada', 'destacada'
    )
    search_fields = ('titulo', 'descripcion', 'reclutador__nombre', 'secretaria__nombre')
    date_hierarchy = 'fecha_publicacion'
    readonly_fields = ('fecha_publicacion', 'fecha_actualizacion')
    inlines = [RequisitoVacanteInline]

    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'categoria', 'secretaria', 'reclutador')
        }),
        ('Condiciones de Trabajo', {
            'fields': ('tipo_empleo', 'modalidad', 'estado', 'ciudad')
        }),
        ('Salario', {
            'fields': ('salario_min', 'salario_max', 'detalles_salario'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_inicio_estimada', 'fecha_limite', 'fecha_publicacion', 'fecha_actualizacion')
        }),
        ('Control', {
            'fields': ('estado_vacante', 'aprobada', 'destacada', 'max_postulantes')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:  # Si estamos editando un objeto existente
            readonly_fields.extend(['secretaria', 'reclutador'])
        return readonly_fields


@admin.register(RequisitoVacante)
class RequisitoVacanteAdmin(admin.ModelAdmin):
    list_display = ('vacante', 'educacion_minima', 'experiencia_minima')
    list_filter = ('vacante__categoria',)
    search_fields = ('vacante__titulo', 'descripcion_requisitos')
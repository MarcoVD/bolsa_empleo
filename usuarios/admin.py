# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Interesado, Reclutador, Secretaria


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
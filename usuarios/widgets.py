# usuarios/widgets.py
from django import forms
from django.utils.safestring import mark_safe
import json


class CurrencyInput(forms.NumberInput):
    """
    Widget personalizado para campos de moneda que maneja formato mexicano.
    """

    def __init__(self, attrs=None, decimal_places=2, max_digits=10):
        self.decimal_places = decimal_places
        self.max_digits = max_digits

        default_attrs = {
            'class': 'form-control currency-input',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Ej: 25000.00'
        }

        if attrs:
            default_attrs.update(attrs)

        super().__init__(attrs=default_attrs)

    def format_value(self, value):
        """
        Formatea el valor para mostrar en el input.
        """
        if value is None or value == '':
            return ''

        try:
            # Convertir a float para formatear
            float_value = float(value)
            # Formatear con 2 decimales
            return f"{float_value:.2f}"
        except (ValueError, TypeError):
            return str(value)

    class Media:
        js = ('js/currency-input.js',)
        css = {
            'all': ('css/currency-input.css',)
        }
# usuarios/fields.py
from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
import re
from .widgets import CurrencyInput


class CurrencyField(forms.DecimalField):
    """
    Campo personalizado para manejar entrada de moneda mexicana.
    Convierte automáticamente valores con formato de miles y decimales.
    """

    def __init__(self, *args, **kwargs):
        # Configurar valores por defecto para moneda mexicana
        kwargs.setdefault('max_digits', 12)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('widget', CurrencyInput())

        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Convierte el valor de entrada a Decimal, manejando formato mexicano.
        """
        if value in self.empty_values:
            return None

        # Si ya es un Decimal, devolverlo
        if isinstance(value, Decimal):
            return value

        # Limpiar el valor de entrada
        if isinstance(value, str):
            # Remover espacios
            value = value.strip()

            # Si está vacío después de limpiar
            if not value:
                return None

            # Limpiar formato de moneda
            value = self.clean_currency_string(value)

        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError(
                'Ingresa un valor numérico válido. Ejemplo: 25000.00',
                code='invalid'
            )

    def clean_currency_string(self, value):
        """
        Limpia una cadena de texto con formato de moneda mexicana.
        Ejemplos:
        - "$25,000.00" -> "25000.00"
        - "25,000.50" -> "25000.50"
        - "25000" -> "25000"
        """
        if not isinstance(value, str):
            return value

        # Remover símbolo de moneda y espacios
        value = re.sub(r'[$\s]', '', value)

        # Remover texto como "MXN", "pesos", etc.
        value = re.sub(r'[a-zA-Z]+', '', value)

        # Manejar formato mexicano: 25,000.50
        # Si hay comas Y puntos, asumir que la coma es separador de miles
        if ',' in value and '.' in value:
            # Verificar que el formato sea correcto (coma antes que punto)
            comma_pos = value.rfind(',')
            dot_pos = value.rfind('.')

            if comma_pos < dot_pos:
                # Formato correcto: 25,000.50
                value = value.replace(',', '')
            else:
                # Formato incorrecto o ambiguo
                raise ValidationError(
                    'Formato de moneda no válido. Usa formato: 25000.50 o 25,000.50',
                    code='invalid_format'
                )

        # Si solo hay comas, pueden ser separadores de miles o decimales
        elif ',' in value and '.' not in value:
            # Contar las comas
            comma_count = value.count(',')

            if comma_count == 1:
                # Una sola coma - verificar posición para determinar uso
                comma_pos = value.find(',')
                after_comma = value[comma_pos + 1:]

                # Si después de la coma hay exactamente 2 dígitos, es decimal
                if len(after_comma) == 2 and after_comma.isdigit():
                    value = value.replace(',', '.')
                # Si hay más de 2 dígitos, es separador de miles
                elif len(after_comma) > 2:
                    value = value.replace(',', '')
                # Si hay menos de 2 dígitos, también tratarlo como decimal
                else:
                    value = value.replace(',', '.')
            else:
                # Múltiples comas - todas son separadores de miles
                value = value.replace(',', '')

        # Validar que el resultado sea un número válido
        if not re.match(r'^\d+(\.\d{1,2})?$', value):
            raise ValidationError(
                'Formato de número no válido. Ejemplo: 25000.50',
                code='invalid_number'
            )

        return value

    def validate(self, value):
        """
        Validaciones adicionales para campos de moneda.
        """
        super().validate(value)

        if value is not None:
            # Validar que sea positivo
            if value < 0:
                raise ValidationError(
                    'El salario debe ser un valor positivo.',
                    code='negative_value'
                )

            # Validar límite máximo razonable (10 millones)
            if value > Decimal('10000000'):
                raise ValidationError(
                    'El salario ingresado es demasiado alto.',
                    code='too_high'
                )

    def prepare_value(self, value):
        """
        Prepara el valor para mostrar en el widget.
        """
        if value is None:
            return ''

        # Convertir a Decimal si no lo es
        if not isinstance(value, Decimal):
            try:
                value = Decimal(str(value))
            except (InvalidOperation, ValueError):
                return str(value)

        # Formatear con 2 decimales
        return f"{value:.2f}"
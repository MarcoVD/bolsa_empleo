// // static/js/currency-input.js
//
// document.addEventListener('DOMContentLoaded', function() {
//     // Inicializar todos los campos de moneda
//     const currencyInputs = document.querySelectorAll('.currency-input');
//
//     currencyInputs.forEach(function(input) {
//         initializeCurrencyInput(input);
//     });
// });
//
// function initializeCurrencyInput(input) {
//     // Formatear valor inicial si existe
//     if (input.value) {
//         input.value = formatCurrencyValue(input.value);
//     }
//
//     // Eventos para formateo en tiempo real
//     input.addEventListener('input', function(e) {
//         const cursorPosition = e.target.selectionStart;
//         const oldValue = e.target.value;
//         const newValue = formatCurrencyInput(oldValue);
//
//         if (newValue !== oldValue) {
//             e.target.value = newValue;
//             // Mantener posición del cursor
//             const newPosition = cursorPosition + (newValue.length - oldValue.length);
//             e.target.setSelectionRange(newPosition, newPosition);
//         }
//     });
//
//     // Formatear al perder el foco
//     input.addEventListener('blur', function(e) {
//         if (e.target.value) {
//             e.target.value = formatCurrencyValue(e.target.value);
//         }
//     });
//
//     // Limpiar formato al enfocar para edición más fácil
//     input.addEventListener('focus', function(e) {
//         const value = e.target.value;
//         if (value) {
//             // Remover formato pero mantener decimales
//             e.target.value = cleanCurrencyValue(value);
//         }
//     });
// }
//
// function formatCurrencyInput(value) {
//     // Permitir solo números, punto decimal
//     let cleanValue = value.replace(/[^\d.]/g, '');
//
//     // Asegurar solo un punto decimal
//     const parts = cleanValue.split('.');
//     if (parts.length > 2) {
//         cleanValue = parts[0] + '.' + parts.slice(1).join('');
//     }
//
//     // Limitar decimales a 2 lugares
//     if (parts[1] && parts[1].length > 2) {
//         cleanValue = parts[0] + '.' + parts[1].substring(0, 2);
//     }
//
//     return cleanValue;
// }
//
// function formatCurrencyValue(value) {
//     // Limpiar el valor
//     const cleanValue = cleanCurrencyValue(value);
//
//     if (!cleanValue || isNaN(cleanValue)) {
//         return '';
//     }
//
//     // Convertir a número y formatear
//     const number = parseFloat(cleanValue);
//
//     // Formatear con separador de miles y 2 decimales
//     return new Intl.NumberFormat('es-MX', {
//         minimumFractionDigits: 2,
//         maximumFractionDigits: 2
//     }).format(number);
// }
//
// function cleanCurrencyValue(value) {
//     if (!value) return '';
//
//     // Remover todo excepto números y punto decimal
//     let cleanValue = value.toString().replace(/[^\d.]/g, '');
//
//     // Si hay múltiples puntos, mantener solo el último
//     const lastDotIndex = cleanValue.lastIndexOf('.');
//     if (lastDotIndex !== -1) {
//         const beforeDot = cleanValue.substring(0, lastDotIndex).replace(/\./g, '');
//         const afterDot = cleanValue.substring(lastDotIndex);
//         cleanValue = beforeDot + afterDot;
//     }
// // En publicar_vacante.html, dentro del script
// document.getElementById('vacanteForm').addEventListener('submit', function() {
//     ['{{ vacante_form.salario_min.id_for_label }}', '{{ vacante_form.salario_max.id_for_label }}'].forEach(function(id) {
//         var input = document.getElementById(id);
//         if (input) {
//             input.value = input.value.replace(/,/g, '').replace(/\$/g, '').trim();
//         }
//     });
// });
//     return cleanValue;
// }
//
// // Función para obtener el valor numérico limpio (útil para validaciones)
// function getCurrencyNumericValue(input) {
//     const cleanValue = cleanCurrencyValue(input.value);
//     return cleanValue ? parseFloat(cleanValue) : null;
// }{{ vacante.salario_min|floatformat:2|intcomma }} MXN
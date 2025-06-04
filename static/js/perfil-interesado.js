// static/js/perfil-interesado.js - Simplificado ya que el cropper maneja el guardado automático
document.addEventListener('DOMContentLoaded', function() {
    const guardarBtn = document.getElementById('guardarPerfilBtn');
    const form = document.getElementById('editarPerfilForm');
    const modal = document.getElementById('editarPerfilModal');

    if (!guardarBtn || !form || !modal) return;

    guardarBtn.addEventListener('click', function() {
        // Validar campos requeridos
        const nombre = form.querySelector('#nombre').value.trim();
        const apellidoPaterno = form.querySelector('#apellido_paterno').value.trim();

        if (!nombre || !apellidoPaterno) {
            mostrarMensaje('Nombre y apellido paterno son obligatorios', 'error');
            return;
        }

        // Mostrar spinner
        const btnText = guardarBtn.querySelector('.btn-text');
        const spinner = guardarBtn.querySelector('.spinner-border');

        btnText.textContent = 'Guardando...';
        spinner.classList.remove('d-none');
        guardarBtn.disabled = true;

        // Crear FormData solo con datos del formulario (sin imagen, ya se guardó automáticamente)
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
        formData.append('nombre', form.querySelector('#nombre').value);
        formData.append('apellido_paterno', form.querySelector('#apellido_paterno').value);
        formData.append('apellido_materno', form.querySelector('#apellido_materno').value);
        formData.append('telefono', form.querySelector('#telefono').value);
        formData.append('fecha_nacimiento', form.querySelector('#fecha_nacimiento').value);
        formData.append('municipio', form.querySelector('#municipio').value);
        formData.append('codigo_postal', form.querySelector('#codigo_postal').value);

        // Obtener URL
        const updateUrl = form.dataset.updateUrl || '/ajax/actualizar-perfil/';

        // Enviar petición AJAX
        fetch(updateUrl, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar información en la página
                actualizarInformacionPerfil(data.data);

                // Mostrar mensaje de éxito
                mostrarMensaje('Perfil actualizado exitosamente', 'success');

                // Cerrar modal
                bootstrap.Modal.getInstance(modal).hide();
            } else {
                mostrarMensaje('Error: ' + (data.error || 'No se pudo actualizar el perfil'), 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarMensaje('Error de conexión. Inténtalo nuevamente.', 'error');
        })
        .finally(() => {
            // Restaurar botón
            btnText.textContent = 'Guardar Cambios';
            spinner.classList.add('d-none');
            guardarBtn.disabled = false;
        });
    });
});

// static/js/perfil-interesado.js - Función actualizarInformacionPerfil corregida

function actualizarInformacionPerfil(data) {
    // Actualizar nombre en el perfil
    const nombreElement = document.querySelector('.card-body h4');
    if (nombreElement && data.nombre_completo) {
        nombreElement.textContent = data.nombre_completo;
    }

    // Actualizar información de contacto
    const contactInfo = document.querySelector('.contact-info');
    if (contactInfo) {
        // Actualizar teléfono
        const telefonoItem = contactInfo.querySelector('.contact-item:nth-child(2)');
        if (telefonoItem && data.telefono) {
            const telefonoSpan = telefonoItem.querySelector('span:last-child');
            if (telefonoSpan) {
                telefonoSpan.textContent = data.telefono;
            }
        }

        // Actualizar ubicación - CORREGIDO PARA EVITAR DUPLICACIÓN
        const ubicacionItem = contactInfo.querySelector('.contact-item:nth-child(3)');
        if (ubicacionItem && data.ubicacion) {
            const ubicacionContainer = ubicacionItem.querySelector('div.flex-grow-1');

            if (ubicacionContainer) {
                // Limpiar todo el contenido de ubicación para evitar duplicados
                ubicacionContainer.innerHTML = '';

                // Crear el contenido de ubicación completo
                const strongElement = document.createElement('strong');
                strongElement.className = 'd-block d-sm-inline small';
                strongElement.textContent = 'Ubicación:';

                const ubicacionSpan = document.createElement('span');

                // Manejar diferentes formatos de ubicación
                if (data.ubicacion.startsWith('C.P.')) {
                    // Formato: "C.P. 56616, Valle de Chalco Solidaridad, Estado de México"
                    ubicacionSpan.textContent = ` ${data.ubicacion}`;
                    ubicacionContainer.appendChild(strongElement);
                    ubicacionContainer.appendChild(ubicacionSpan);
                } else if (data.ubicacion.includes(' C.P. ')) {
                    // Formato: "Valle de Chalco Solidaridad, Estado de México C.P. 56616"
                    const parts = data.ubicacion.split(' C.P. ');
                    const ubicacionSinCP = parts[0];
                    const codigoPostal = parts[1];

                    if (codigoPostal && codigoPostal !== 'undefined') {
                        ubicacionSpan.textContent = ` ${ubicacionSinCP}`;

                        // Crear elemento del código postal
                        const cpElement = document.createElement('small');
                        cpElement.className = 'd-block text-muted';
                        cpElement.textContent = `C.P. ${codigoPostal}`;

                        // Añadir elementos al contenedor
                        ubicacionContainer.appendChild(strongElement);
                        ubicacionContainer.appendChild(ubicacionSpan);
                        ubicacionContainer.appendChild(cpElement);
                    } else {
                        // Si el código postal está undefined, solo mostrar la ubicación
                        ubicacionSpan.textContent = ` ${ubicacionSinCP}`;
                        ubicacionContainer.appendChild(strongElement);
                        ubicacionContainer.appendChild(ubicacionSpan);
                    }
                } else {
                    // Solo ubicación sin código postal
                    ubicacionSpan.textContent = ` ${data.ubicacion}`;
                    ubicacionContainer.appendChild(strongElement);
                    ubicacionContainer.appendChild(ubicacionSpan);
                }
            }
        }
    }

    // Actualizar foto de perfil principal y en información móvil
    if (data.foto_url) {
        const fotoElements = document.querySelectorAll('.profile-photo');
        const placeholderElements = document.querySelectorAll('.profile-photo-placeholder');

        fotoElements.forEach(el => el.src = data.foto_url);

        placeholderElements.forEach(placeholder => {
            const imgElement = document.createElement('img');
            imgElement.src = data.foto_url;
            imgElement.alt = 'Foto de perfil';
            imgElement.className = 'profile-photo';
            placeholder.parentNode.replaceChild(imgElement, placeholder);
        });
    }
}


function mostrarMensaje(mensaje, tipo) {
    // Crear contenedor de toasts si no existe
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed bottom-0 start-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }

    // Crear toast
    const toastId = 'toast-' + Date.now();
    const toastDiv = document.createElement('div');
    toastDiv.id = toastId;
    toastDiv.className = `toast align-items-center text-bg-${tipo === 'success' ? 'success' : 'danger'} border-0`;
    toastDiv.setAttribute('role', 'alert');
    toastDiv.setAttribute('aria-live', 'assertive');
    toastDiv.setAttribute('aria-atomic', 'true');

    toastDiv.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-${tipo === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
                ${mensaje}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toastDiv);

    // Mostrar toast
    const toast = new bootstrap.Toast(toastDiv, {
        autohide: true,
        delay: 4000
    });
    toast.show();

    // Remover del DOM después de que se oculte
    toastDiv.addEventListener('hidden.bs.toast', function() {
        toastDiv.remove();
    });
}
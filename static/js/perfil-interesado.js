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
        const telefonoSpan = contactInfo.querySelector('.contact-item:nth-child(2) span:last-child');
        if (telefonoSpan && data.telefono) {
            telefonoSpan.textContent = data.telefono;
        }

        // Actualizar ubicación
        const ubicacionSpan = contactInfo.querySelector('.contact-item:nth-child(3) span:first-of-type');
        if (ubicacionSpan && data.ubicacion) {
            const ubicacionSinCP = data.ubicacion.split(' C.P.')[0];
            ubicacionSpan.textContent = ubicacionSinCP;

            // Manejar código postal
            const cpElement = ubicacionSpan.nextElementSibling;
            if (data.ubicacion.includes('C.P.')) {
                const cp = data.ubicacion.split('C.P. ')[1];
                if (cpElement && cpElement.classList.contains('text-muted')) {
                    cpElement.textContent = `C.P. ${cp}`;
                } else {
                    // Crear elemento de código postal si no existe
                    const newCpElement = document.createElement('small');
                    newCpElement.className = 'd-block text-muted';
                    newCpElement.textContent = `C.P. ${cp}`;
                    ubicacionSpan.parentNode.appendChild(newCpElement);
                }
            } else if (cpElement && cpElement.classList.contains('text-muted')) {
                // Remover código postal si no existe
                cpElement.remove();
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
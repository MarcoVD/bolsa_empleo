// static/js/perfil-interesado.js - Archivo completo actualizado
document.addEventListener('DOMContentLoaded', function() {
    const guardarBtn = document.getElementById('guardarPerfilBtn');
    const form = document.getElementById('editarPerfilForm');
    const modal = document.getElementById('editarPerfilModal');
    const fotoInput = document.getElementById('foto_perfil');

    if (!guardarBtn || !form || !modal) return;

    // Validación de archivo JPG
    if (fotoInput) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar extensión
                const validTypes = ['image/jpeg', 'image/jpg'];
                if (!validTypes.includes(file.type)) {
                    mostrarMensaje('Solo se permiten archivos JPG', 'error');
                    e.target.value = '';
                    return;
                }

                // Validar tamaño (5MB)
                if (file.size > 5 * 1024 * 1024) {
                    mostrarMensaje('El archivo es demasiado grande. Máximo 5MB', 'error');
                    e.target.value = '';
                    return;
                }
            }
        });
    }

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

        // Crear FormData
        const formData = new FormData(form);

        // Obtener URL y CSRF token
        const updateUrl = form.dataset.updateUrl || '/ajax/actualizar-perfil/';
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Enviar petición AJAX
        fetch(updateUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
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

                // Limpiar input de archivo
                if (fotoInput) fotoInput.value = '';
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
    const nombreElement = document.querySelector('.profile-photo-container + h4, .profile-photo-container + h5');
    if (nombreElement && data.nombre_completo) {
        nombreElement.textContent = data.nombre_completo;
    }

    // Actualizar teléfono
    const telefonoElements = document.querySelectorAll('.contact-info .contact-item:nth-child(2) span:last-child');
    if (telefonoElements.length > 0 && data.telefono) {
        telefonoElements[0].textContent = data.telefono;
    }

    // Actualizar ubicación - CORREGIDO
    const ubicacionElements = document.querySelectorAll('.contact-info .contact-item:nth-child(3) span:not(.text-muted)');
    if (ubicacionElements.length > 0 && data.ubicacion) {
        ubicacionElements[0].textContent = data.ubicacion;
    }

    // Actualizar foto de perfil si existe
    if (data.foto_url) {
        const fotoElement = document.querySelector('.profile-photo');
        const placeholderElement = document.querySelector('.profile-photo-placeholder');

        if (fotoElement) {
            fotoElement.src = data.foto_url;
        } else if (placeholderElement) {
            // Reemplazar placeholder con imagen real
            const imgElement = document.createElement('img');
            imgElement.src = data.foto_url;
            imgElement.alt = 'Foto de perfil';
            imgElement.className = 'profile-photo img-fluid rounded-circle';
            placeholderElement.parentNode.replaceChild(imgElement, placeholderElement);
        }
    }
}

aqui


function mostrarMensaje(mensaje, tipo) {
    // Crear contenedor de toasts si no existe
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }

    // Crear toast
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${tipo === 'success' ? 'bg-success text-white' : 'bg-danger text-white'}">
                <i class="bi bi-${tipo === 'success' ? 'check-circle-fill' : 'exclamation-triangle-fill'} me-2"></i>
                <strong class="me-auto">${tipo === 'success' ? 'Éxito' : 'Error'}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${mensaje}
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    // Inicializar y mostrar toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 4000
    });

    toast.show();

    // Remover elemento después de ocultar
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}
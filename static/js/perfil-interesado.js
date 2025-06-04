// static/js/perfil-interesado.js - Archivo completo actualizado
// document.addEventListener('DOMContentLoaded', function() {
//     const guardarBtn = document.getElementById('guardarPerfilBtn');
//     const form = document.getElementById('editarPerfilForm');
//     const modal = document.getElementById('editarPerfilModal');
//     const fotoInput = document.getElementById('foto_perfil');
//
//     if (!guardarBtn || !form || !modal) return;
//
//     // Validación de archivo JPG
//     if (fotoInput) {
//         fotoInput.addEventListener('change', function(e) {
//             const file = e.target.files[0];
//             if (file) {
//                 // Validar extensión
//                 const validTypes = ['image/jpeg', 'image/jpg'];
//                 if (!validTypes.includes(file.type)) {
//                     mostrarMensaje('Solo se permiten archivos JPG', 'error');
//                     e.target.value = '';
//                     return;
//                 }
//
//                 // Validar tamaño (5MB)
//                 if (file.size > 5 * 1024 * 1024) {
//                     mostrarMensaje('El archivo es demasiado grande. Máximo 5MB', 'error');
//                     e.target.value = '';
//                     return;
//                 }
//             }
//         });
//     }
//
//     guardarBtn.addEventListener('click', function() {
//         // Validar campos requeridos
//         const nombre = form.querySelector('#nombre').value.trim();
//         const apellidoPaterno = form.querySelector('#apellido_paterno').value.trim();
//
//         if (!nombre || !apellidoPaterno) {
//             mostrarMensaje('Nombre y apellido paterno son obligatorios', 'error');
//             return;
//         }
//
//         // Mostrar spinner
//         const btnText = guardarBtn.querySelector('.btn-text');
//         const spinner = guardarBtn.querySelector('.spinner-border');
//
//         btnText.textContent = 'Guardando...';
//         spinner.classList.remove('d-none');
//         guardarBtn.disabled = true;
//
//         // Crear FormData
//         const formData = new FormData(form);
//
//         // Obtener URL y CSRF token
//         const updateUrl = form.dataset.updateUrl || '/ajax/actualizar-perfil/';
//         const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//
//         // Enviar petición AJAX
//         fetch(updateUrl, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': csrfToken
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 // Actualizar información en la página
//                 actualizarInformacionPerfil(data.data);
//
//                 // Mostrar mensaje de éxito
//                 mostrarMensaje('Perfil actualizado exitosamente', 'success');
//
//                 // Cerrar modal
//                 bootstrap.Modal.getInstance(modal).hide();
//
//                 // Limpiar input de archivo
//                 if (fotoInput) fotoInput.value = '';
//             } else {
//                 mostrarMensaje('Error: ' + (data.error || 'No se pudo actualizar el perfil'), 'error');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             mostrarMensaje('Error de conexión. Inténtalo nuevamente.', 'error');
//         })
//         .finally(() => {
//             // Restaurar botón
//             btnText.textContent = 'Guardar Cambios';
//             spinner.classList.add('d-none');
//             guardarBtn.disabled = false;
//         });
//     });
// });


// function actualizarInformacionPerfil(data) {
//     // Actualizar nombre en el perfil
//     const nombreElement = document.querySelector('.profile-photo-container + h4, .profile-photo-container + h5');
//     if (nombreElement && data.nombre_completo) {
//         nombreElement.textContent = data.nombre_completo;
//     }
//
//     // Actualizar teléfono
//     const telefonoElements = document.querySelectorAll('.contact-info .contact-item:nth-child(2) span:last-child');
//     if (telefonoElements.length > 0 && data.telefono) {
//         telefonoElements[0].textContent = data.telefono;
//     }
//
//     // Actualizar ubicación - CORREGIDO
//     const ubicacionElements = document.querySelectorAll('.contact-info .contact-item:nth-child(3) span:not(.text-muted)');
//     if (ubicacionElements.length > 0 && data.ubicacion) {
//         ubicacionElements[0].textContent = data.ubicacion;
//     }
//
//     // Actualizar foto de perfil si existe
//     if (data.foto_url) {
//         const fotoElement = document.querySelector('.profile-photo');
//         const placeholderElement = document.querySelector('.profile-photo-placeholder');
//
//         if (fotoElement) {
//             fotoElement.src = data.foto_url;
//         } else if (placeholderElement) {
//             // Reemplazar placeholder con imagen real
//             const imgElement = document.createElement('img');
//             imgElement.src = data.foto_url;
//             imgElement.alt = 'Foto de perfil';
//             imgElement.className = 'profile-photo img-fluid rounded-circle';
//             placeholderElement.parentNode.replaceChild(imgElement, placeholderElement);
//         }
//     }
// }
// static/js/perfil-interesado.js - Función mostrarMensaje actualizada - toast
// function mostrarMensaje(mensaje, tipo) {
//     // Crear contenedor de toasts si no existe
//     let toastContainer = document.getElementById('toast-container');
//     if (!toastContainer) {
//         toastContainer = document.createElement('div');
//         toastContainer.id = 'toast-container';
//         toastContainer.className = 'toast-container position-fixed bottom-0 start-0 p-3';
//         toastContainer.style.zIndex = '1055';
//         document.body.appendChild(toastContainer);
//     }
//
//     // Crear toast
//     const toastId = 'toast-' + Date.now();
//     const toastDiv = document.createElement('div');
//     toastDiv.id = toastId;
//     toastDiv.className = `toast align-items-center text-bg-${tipo === 'success' ? 'success' : 'danger'} border-0`;
//     toastDiv.setAttribute('role', 'alert');
//     toastDiv.setAttribute('aria-live', 'assertive');
//     toastDiv.setAttribute('aria-atomic', 'true');
//
//     toastDiv.innerHTML = `
//         <div class="d-flex">
//             <div class="toast-body">
//                 <i class="bi bi-${tipo === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
//                 ${mensaje}
//             </div>
//             <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
//         </div>
//     `;
//
//     toastContainer.appendChild(toastDiv);
//
//     // Mostrar toast
//     const toast = new bootstrap.Toast(toastDiv, {
//         autohide: true,
//         delay: 4000
//     });
//     toast.show();
//
//     // Remover del DOM después de que se oculte
//     toastDiv.addEventListener('hidden.bs.toast', function() {
//         toastDiv.remove();
//     });
// }

// static/js/perfil-interesado.js - Actualizado con integración del cropper
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

        // Crear FormData
        const formData = new FormData(form);

        // Si hay una imagen recortada, reemplazar el archivo original
        if (window.imageCropper && window.imageCropper.getCroppedFile()) {
            const croppedFile = window.imageCropper.getCroppedFile();
            formData.delete('foto_perfil');
            formData.append('foto_perfil', croppedFile, 'profile.jpg');
        }

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

                // Limpiar cropper
                if (window.imageCropper) {
                    window.imageCropper.croppedBlob = null;
                }
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
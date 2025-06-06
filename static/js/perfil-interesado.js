// static/js/perfil-interesado.js - Simplificado ya que el cropper maneja el guardado automático

// Agregar este JavaScript al final de perfil_interesado.html o en un archivo separado

document.addEventListener('DOMContentLoaded', function() {
    const profilePhotoContainer = document.getElementById('profilePhotoClick');
    const fileInput = document.getElementById('foto_perfil');
    const photoOverlay = document.querySelector('.photo-overlay');

    // Efecto hover en la foto
    profilePhotoContainer.addEventListener('mouseenter', function() {
        photoOverlay.style.opacity = '1';
    });

    profilePhotoContainer.addEventListener('mouseleave', function() {
        photoOverlay.style.opacity = '0';
    });

    // Click en la foto abre selector de archivo
    profilePhotoContainer.addEventListener('click', function() {
        fileInput.click();
    });

    // Cuando se selecciona un archivo
    fileInput.addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];

            // Validar tipo de archivo
            if (!file.type.match(/^image\/(jpeg|jpg)$/)) {
                showErrorMessage('Por favor selecciona una imagen en formato JPG');
                return;
            }

            // Validar tamaño (5MB máximo)
            if (file.size > 5 * 1024 * 1024) {
                showErrorMessage('La imagen no debe superar los 5MB');
                return;
            }

            // Cargar imagen y procesar
            const reader = new FileReader();
            reader.onload = function(event) {
                loadImageInCropper(event.target.result);

                // Mostrar modal del cropper directamente
                const cropperModal = new bootstrap.Modal(document.getElementById('cropperModal'));
                cropperModal.show();

                // Ir directamente al paso de recorte
                showCropStep();
            };
            reader.readAsDataURL(file);
        }
    });
});

function loadImageInCropper(imageSrc) {
    const cropperImage = document.getElementById('cropperImage');

    // Destruir cropper anterior si existe
    if (window.cropper) {
        window.cropper.destroy();
    }

    // Cargar nueva imagen
    cropperImage.src = imageSrc;
    cropperImage.style.display = 'block';

    // Inicializar nuevo cropper
    window.cropper = new Cropper(cropperImage, {
        aspectRatio: 1,
        viewMode: 1,
        dragMode: 'move',
        autoCropArea: 0.8,
        restore: false,
        guides: false,
        center: false,
        highlight: false,
        cropBoxMovable: true,
        cropBoxResizable: true,
        toggleDragModeOnDblclick: false,
        preview: '#cropPreview'
    });
}

function showCropStep() {
    document.getElementById('selectStep').classList.remove('active');
    document.getElementById('cropStep').classList.add('active');
}

// Función para el botón "Recortar y Usar" (modificada para cerrar modal y guardar automáticamente)
// Agregar/modificar en el script del perfil_interesado.html o en tu archivo JS

// Función para el botón "Recortar y Usar" - SIMPLIFICADA
document.getElementById('cropButton').addEventListener('click', function() {
    if (window.cropper) {
        // Obtener la imagen recortada
        const canvas = window.cropper.getCroppedCanvas({
            width: 160,
            height: 160,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high'
        });

        if (canvas) {
            // Convertir a blob
            canvas.toBlob(function(blob) {
                // Crear FormData para envío inmediato
                const formData = new FormData();
                formData.append('foto_perfil', blob, 'profile_photo.jpg');
                formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

                // Actualizar preview inmediatamente en la página principal
                const imageUrl = canvas.toDataURL('image/jpeg', 0.9);
                updateMainProfilePhoto(imageUrl);

                // Cerrar modal del cropper
                const cropperModal = bootstrap.Modal.getInstance(document.getElementById('cropperModal'));
                if (cropperModal) {
                    cropperModal.hide();
                }

                // Guardar automáticamente
                saveProfilePhoto(formData);

                // Limpiar el input file
                document.getElementById('foto_perfil').value = '';

            }, 'image/jpeg', 0.9);
        }
    }
});

// Función para resetear el cropper
document.getElementById('resetCropButton').addEventListener('click', function() {
    if (window.cropper) {
        window.cropper.reset();
    }
});

// Función para cancelar
document.getElementById('cancelCropButton').addEventListener('click', function() {
    const cropperModal = bootstrap.Modal.getInstance(document.getElementById('cropperModal'));
    if (cropperModal) {
        cropperModal.hide();
    }

    // Limpiar el input file
    document.getElementById('foto_perfil').value = '';

    // Destruir cropper
    if (window.cropper) {
        window.cropper.destroy();
        window.cropper = null;
    }
});

// Función para actualizar solo la foto principal (sin modal)
function updateMainPhotoPreview(imageUrl) {
    const mainPhotoContainer = document.querySelector('.profile-photo-container');
    const existingImg = mainPhotoContainer.querySelector('.profile-photo');
    const placeholder = mainPhotoContainer.querySelector('.profile-photo-placeholder');

    if (existingImg) {
        existingImg.src = imageUrl;
    } else {
        // Crear nueva imagen si no existe
        const newImg = document.createElement('img');
        newImg.src = imageUrl;
        newImg.alt = 'Foto de perfil';
        newImg.className = 'profile-photo img-fluid rounded-circle';

        // Ocultar placeholder y agregar imagen
        if (placeholder) {
            placeholder.style.display = 'none';
        }

        mainPhotoContainer.insertBefore(newImg, mainPhotoContainer.firstChild);
    }
}

// Función para guardar la foto directamente
function saveProfilePhotoDirectly(formData) {
    // Mostrar indicador de carga
    showSaveIndicator();

    // URL para actualizar solo la foto (necesitarás crear esta vista)
    const updateUrl = "{% url 'actualizar_foto_perfil_ajax' %}"; // Nueva URL específica para foto

    fetch(updateUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        hideSaveIndicator();

        if (data.success) {
            showSuccessMessage('Foto de perfil actualizada correctamente');

            // Actualizar con la URL real del servidor
            if (data.photo_url) {
                updateMainPhotoPreview(data.photo_url);
            }
        } else {
            showErrorMessage('Error al guardar la foto: ' + (data.error || 'Error desconocido'));
        }
    })
    .catch(error => {
        hideSaveIndicator();
        console.error('Error:', error);
        showErrorMessage('Error de conexión al guardar la foto');
    });
}

// Funciones auxiliares (mantener las mismas del código anterior)
function showSaveIndicator() {
    let indicator = document.getElementById('saveIndicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'saveIndicator';
        indicator.className = 'position-fixed top-0 end-0 m-3 alert alert-info d-flex align-items-center';
        indicator.style.zIndex = '9999';
        indicator.innerHTML = `
            <div class="spinner-border spinner-border-sm me-2" role="status"></div>
            Guardando foto...
        `;
        document.body.appendChild(indicator);
    }
    indicator.style.display = 'flex';
}

function hideSaveIndicator() {
    const indicator = document.getElementById('saveIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

function showSuccessMessage(message) {
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 end-0 m-3 alert alert-success alert-dismissible';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <i class="bi bi-check-circle-fill me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

function showErrorMessage(message) {
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 end-0 m-3 alert alert-danger alert-dismissible';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

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
// JavaScript actualizado para perfil_interesado.html

// Función para guardar la foto directamente (ACTUALIZADA)
function saveProfilePhotoDirectly(formData) {
    // Mostrar indicador de carga
    showSaveIndicator();

    // URL para actualizar solo la foto
    const updateUrl = "{% url 'actualizar_foto_perfil_ajax' %}";

    fetch(updateUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        hideSaveIndicator();

        if (data.success) {
            showSuccessMessage('Foto de perfil actualizada correctamente');

            // Actualizar con la URL real del servidor
            if (data.photo_url) {
                updateMainPhotoPreview(data.photo_url);
            }
        } else {
            showErrorMessage('Error al guardar la foto: ' + (data.error || 'Error desconocido'));
        }
    })
    .catch(error => {
        hideSaveIndicator();
        console.error('Error:', error);
        showErrorMessage('Error de conexión al guardar la foto');
    });
}

// El resto del JavaScript se mantiene igual...


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
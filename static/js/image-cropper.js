// static/js/image-cropper.js
class ImageCropper {
    constructor() {
        this.cropper = null;
        this.currentFile = null;
        this.croppedBlob = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        const fileInput = document.getElementById('foto_perfil');
        const dropZone = document.getElementById('dropZone');

        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }

        if (dropZone) {
            dropZone.addEventListener('click', () => fileInput?.click());
            dropZone.addEventListener('dragover', (e) => this.handleDragOver(e));
            dropZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
            dropZone.addEventListener('drop', (e) => this.handleDrop(e));
        }

        // Botones del cropper
        document.addEventListener('click', (e) => {
            if (e.target.id === 'cropButton') this.cropImage();
            if (e.target.id === 'resetCropButton') this.resetCropper();
            if (e.target.id === 'cancelCropButton') this.cancelCrop();
        });
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('dragover');
    }

    handleDragLeave(event) {
        event.currentTarget.classList.remove('dragover');
    }

    handleDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    processFile(file) {
        // Validar tipo de archivo
        if (!file.type.match(/^image\/(jpeg|jpg)$/i)) {
            this.showMessage('Solo se permiten archivos JPG', 'error');
            return;
        }

        // Validar tamaño (5MB)
        if (file.size > 5 * 1024 * 1024) {
            this.showMessage('El archivo es demasiado grande. Máximo 5MB', 'error');
            return;
        }

        this.currentFile = file;
        this.loadImageForCropping(file);
    }

    loadImageForCropping(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.showCropperStep();
            this.initializeCropper(e.target.result);
        };
        reader.readAsDataURL(file);
    }

    showCropperStep() {
        document.getElementById('selectStep').classList.remove('active');
        document.getElementById('cropStep').classList.add('active');
    }

    showSelectStep() {
        document.getElementById('cropStep').classList.remove('active');
        document.getElementById('selectStep').classList.add('active');
        this.destroyCropper();
    }

    initializeCropper(imageSrc) {
        const imageElement = document.getElementById('cropperImage');
        imageElement.src = imageSrc;

        // Destruir cropper existente si hay uno
        this.destroyCropper();

        // Inicializar nuevo cropper
        this.cropper = new Cropper(imageElement, {
            aspectRatio: 1, // Cuadrado 1:1
            viewMode: 1,
            dragMode: 'move',
            autoCropArea: 0.8,
            restore: false,
            guides: true,
            center: true,
            highlight: false,
            cropBoxMovable: true,
            cropBoxResizable: true,
            toggleDragModeOnDblclick: false,
            modal: true,
            background: true,
            responsive: true,
            checkOrientation: false,
            minCropBoxWidth: 100,
            minCropBoxHeight: 100,
            ready: () => {
                this.updatePreview();
            },
            cropend: () => {
                this.updatePreview();
            }
        });
    }

    updatePreview() {
        if (!this.cropper) return;

        const canvas = this.cropper.getCroppedCanvas({
            width: 160,
            height: 160,
            fillColor: '#fff',
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high'
        });

        const previewContainer = document.getElementById('cropPreview');
        const previewImg = previewContainer.querySelector('img');

        if (previewImg) {
            previewImg.src = canvas.toDataURL('image/jpeg', 0.9);
        } else {
            const img = document.createElement('img');
            img.src = canvas.toDataURL('image/jpeg', 0.9);
            img.alt = 'Preview';
            previewContainer.appendChild(img);
        }

        previewContainer.style.display = 'block';
    }

    cropImage() {
        if (!this.cropper) return;

        const canvas = this.cropper.getCroppedCanvas({
            width: 160,
            height: 160,
            fillColor: '#fff',
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high'
        });

        canvas.toBlob((blob) => {
            this.croppedBlob = blob;
            const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
            this.updateMainPreview(dataUrl);
            this.closeCropperModal();

            // Guardar automáticamente la imagen recortada
            this.saveImageAutomatically(blob, dataUrl);
        }, 'image/jpeg', 0.9);
    }

    updateMainPreview(dataUrl) {
        // Actualizar preview en el modal principal
        const mainPreviewContainer = document.getElementById('photoPreviewContainer');
        const mainPhotoPreview = document.getElementById('photoPreview');
        const mainPhotoPlaceholder = document.getElementById('photoPlaceholder');

        if (mainPhotoPreview) {
            mainPhotoPreview.src = dataUrl;
        } else if (mainPhotoPlaceholder) {
            const imgElement = document.createElement('img');
            imgElement.src = dataUrl;
            imgElement.alt = 'Foto de perfil';
            imgElement.className = 'profile-photo';
            imgElement.id = 'photoPreview';
            mainPreviewContainer.replaceChild(imgElement, mainPhotoPlaceholder);
        }
    }

    resetCropper() {
        if (this.cropper) {
            this.cropper.reset();
            this.updatePreview();
        }
    }

    cancelCrop() {
        this.showSelectStep();
        document.getElementById('foto_perfil').value = '';
        document.getElementById('cropPreview').style.display = 'none';
    }

    destroyCropper() {
        if (this.cropper) {
            this.cropper.destroy();
            this.cropper = null;
        }
    }

    closeCropperModal() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('cropperModal'));
        if (modal) {
            modal.hide();
        }

        // Regresar al modal principal después de cerrar el cropper
        setTimeout(() => {
            const mainModal = new bootstrap.Modal(document.getElementById('editarPerfilModal'));
            mainModal.show();
        }, 300);
    }

    saveImageAutomatically(blob, dataUrl) {
        // Mostrar mensaje de guardando
        this.showMessage('Guardando imagen...', 'info');

        // Crear FormData solo con la imagen
        const formData = new FormData();
        formData.append('foto_perfil', blob, 'profile.jpg');

        // Obtener token CSRF
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const updateUrl = document.getElementById('editarPerfilForm').dataset.updateUrl || '/ajax/actualizar-perfil/';

        // Enviar solo la imagen
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
                // Actualizar todas las imágenes en la página con la nueva URL
                this.updateAllProfileImages(data.data.foto_url || dataUrl);
                this.showMessage('Imagen guardada exitosamente', 'success');
            } else {
                this.showMessage('Error al guardar: ' + (data.error || 'Error desconocido'), 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.showMessage('Error de conexión al guardar la imagen', 'error');
        });
    }

    updateAllProfileImages(imageUrl) {
        // Actualizar imagen en el card principal del perfil
        const mainProfileImages = document.querySelectorAll('.profile-photo');
        const mainProfilePlaceholders = document.querySelectorAll('.profile-photo-placeholder');

        // Actualizar imágenes existentes
        mainProfileImages.forEach(img => {
            img.src = imageUrl;
        });

        // Reemplazar placeholders con imágenes
        mainProfilePlaceholders.forEach(placeholder => {
            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            imgElement.alt = 'Foto de perfil';
            imgElement.className = 'profile-photo';
            placeholder.parentNode.replaceChild(imgElement, placeholder);
        });

        // También actualizar en el modal si está abierto
        const modalPreview = document.getElementById('photoPreview');
        const modalPlaceholder = document.getElementById('photoPlaceholder');

        if (modalPreview) {
            modalPreview.src = imageUrl;
        } else if (modalPlaceholder) {
            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            imgElement.alt = 'Foto de perfil';
            imgElement.className = 'profile-photo';
            imgElement.id = 'photoPreview';
            modalPlaceholder.parentNode.replaceChild(imgElement, modalPlaceholder);
        }
    }

    getCroppedFile() {
        return this.croppedBlob;
    }

    showMessage(mensaje, tipo) {
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

        let bgClass = 'success';
        let icon = 'check-circle';

        switch(tipo) {
            case 'error':
                bgClass = 'danger';
                icon = 'exclamation-circle';
                break;
            case 'info':
                bgClass = 'info';
                icon = 'info-circle';
                break;
            case 'warning':
                bgClass = 'warning';
                icon = 'exclamation-triangle';
                break;
        }

        toastDiv.className = `toast align-items-center text-bg-${bgClass} border-0`;
        toastDiv.setAttribute('role', 'alert');
        toastDiv.setAttribute('aria-live', 'assertive');
        toastDiv.setAttribute('aria-atomic', 'true');

        toastDiv.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${icon} me-2"></i>
                    ${mensaje}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        toastContainer.appendChild(toastDiv);

        // Mostrar toast
        const toast = new bootstrap.Toast(toastDiv, {
            autohide: true,
            delay: tipo === 'info' ? 2000 : 4000
        });
        toast.show();

        // Remover del DOM después de que se oculte
        toastDiv.addEventListener('hidden.bs.toast', function() {
            toastDiv.remove();
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.imageCropper = new ImageCropper();
});
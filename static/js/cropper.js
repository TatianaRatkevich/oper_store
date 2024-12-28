document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.image-zoom');
    let cropperInstance = null;

    images.forEach(img => {
        img.addEventListener('click', () => {
            // Удаление предыдущего модального окна, если оно существует
            const existingModal = document.getElementById('imageModal');
            if (existingModal) {
                if (cropperInstance) {
                    cropperInstance.destroy();
                }
                existingModal.remove();
            }

            // Создание нового модального окна
            const modal = document.createElement('div');
            modal.id = 'imageModal';
            modal.style.position = 'fixed';
            modal.style.top = 0;
            modal.style.left = 0;
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            modal.style.zIndex = 9999;
            modal.style.display = 'flex';
            modal.style.justifyContent = 'center';
            modal.style.alignItems = 'center';
            modal.innerHTML = `
                <div style="position: relative; width: 100%; height: 100%;">
                    <img src="${img.dataset.full}" id="modal-image" style="max-width: 80%; max-height: 80%;">
                    <button style="position: absolute; top: 20px; right: 20px;" class="btn btn-danger btn-sm">Закрыть</button>
                    <button style="position: absolute; top: 20px; left: 20px;" class="btn btn-secondary btn-sm" id="rotate-left">Поворот влево</button>
                    <button style="position: absolute; top: 20px; left: 200px;" class="btn btn-secondary btn-sm" id="rotate-right">Поворот вправо</button>
                </div>
            `;
            document.body.appendChild(modal);

            const closeButton = modal.querySelector('.btn-danger');
            closeButton.addEventListener('click', () => {
                if (cropperInstance) {
                    cropperInstance.destroy();
                }
                modal.remove();
            });

            const rotateLeftButton = modal.querySelector('#rotate-left');
            const rotateRightButton = modal.querySelector('#rotate-right');
            const modalImage = modal.querySelector('#modal-image');

            if (modalImage) {
                cropperInstance = new Cropper(modalImage, {
                    dragMode: 'move',
                    zoomable: true,
                    rotatable: true,
                    scalable: true,
                    wheelZoomRatio: 0.1,
                    movable: true,
                    viewMode: 3,
                });

                rotateLeftButton.addEventListener('click', () => {
                    cropperInstance.rotate(-90);
                });

                rotateRightButton.addEventListener('click', () => {
                    cropperInstance.rotate(90);
                });
            } else {
                console.error('Element with id #modal-image not found');
            }

            // Обновление размеров модального окна при изменении размеров окна браузера
            window.addEventListener('resize', () => {
                modal.style.width = '100%';
                modal.style.height = '100%';
            });
        });
    });
});

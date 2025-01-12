let rotation = 0;

function rotateImage() {
    rotation = (rotation + 90) % 360;
    const image = document.getElementById('rotatable-image');
    image.style.transform = `rotate(${rotation}deg)`;
}

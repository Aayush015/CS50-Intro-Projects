const video = document.getElementById('background-video');
const soundButton = document.getElementById('sound-button');

function toggleSound() {
  video.muted = !video.muted;
}

video.addEventListener('canplay', function() {
  video.play();
});
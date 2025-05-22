document.addEventListener('DOMContentLoaded', () => {
  // Carrossel automático
  const images = document.querySelectorAll('#carousel img');
  let index = 0;

  setInterval(() => {
    images.forEach(img => img.classList.remove('active'));
    index = (index + 1) % images.length;
    images[index].classList.add('active');
  }, 3000);

  // Toggle menu mobile
  window.toggleMenu = function () {
    document.getElementById('navMenu').classList.toggle('show');
  };
});

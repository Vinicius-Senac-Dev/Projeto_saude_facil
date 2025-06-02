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

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.menu-item').forEach(item => {
    const mainLink = item.querySelector('a');
    const submenuLinks = item.querySelectorAll('.submenu a');
    const width = getComputedStyle(mainLink).width;

    submenuLinks.forEach(link => {
      link.style.width = width;
    });
  });
});

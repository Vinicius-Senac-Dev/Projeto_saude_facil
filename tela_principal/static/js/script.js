document.addEventListener('DOMContentLoaded', () => {
  // Carrossel automático
  const images = document.querySelectorAll('#carousel img');
  if (images.length > 0) {
    let index = 0;

    setInterval(() => {
      images.forEach(img => img.classList.remove('active'));
      index = (index + 1) % images.length;
      images[index].classList.add('active');
    }, 3000);
  }

  // Toggle menu mobile
  window.toggleMenu = function () {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
      navMenu.classList.toggle('show');
    }
  };

  // Fechar o menu quando clicar fora dele
  document.addEventListener('click', function(event) {
    const navMenu = document.getElementById('navMenu');
    const menuToggle = document.querySelector('.menu-toggle');
    
    if (navMenu && navMenu.classList.contains('show') && 
        !navMenu.contains(event.target) && 
        !menuToggle.contains(event.target)) {
      navMenu.classList.remove('show');
    }
  });

  // Adicionar classe active ao item de menu atual
  const currentPath = window.location.pathname;
  const menuLinks = document.querySelectorAll('nav a');
  
  menuLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath === href) {
      link.classList.add('active');
    }
  });
});

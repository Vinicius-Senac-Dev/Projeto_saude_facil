// Carrossel automático
const images = document.querySelectorAll('#carousel img');
let index = 0;

setInterval(() => {
  images[index].classList.remove('active');
  index = (index + 1) % images.length;
  images[index].classList.add('active');
}, 3000);

// Notificações toggle
const bell = document.getElementById('notificationBell');
const menu = document.getElementById('notificationMenu');

bell.addEventListener('click', () => {
  menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
});

document.addEventListener('click', function (event) {
  if (!bell.contains(event.target) && !menu.contains(event.target)) {
    menu.style.display = 'none';
  }
});

// Toggle menu mobile
function toggleMenu() {
  document.getElementById('navMenu').classList.toggle('show');
}

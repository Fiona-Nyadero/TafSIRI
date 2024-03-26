const carouselContainer = document.querySelector('.hero-section');
const slides = document.querySelectorAll('.carousel-slide');

let currentIndex = 0;

function showSlide(index) {
  const distance = -index * 100 + '%';
  carouselContainer.style.transform = 'translateX(' + distance + ')';
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
}

function prevSlide() {
  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  showSlide(currentIndex);
}

setInterval(nextSlide, 3000); // Auto slide every 3 seconds

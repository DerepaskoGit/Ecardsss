


document.getElementById('generateInviteBtn').onclick = function() {
  const UrlContainer = document.getElementById("url-container")
  const MyUrl = UrlContainer.dataset.url;
  
  const CsrfContainer = document.getElementById("csrf-container")
  const MyCsrf = CsrfContainer.dataset.csrf;
  
  fetch(MyUrl, {
    method: "POST",
    headers: {
      "X-CSRFToken": MyCsrf,  // CSRF-токен
      "Content-Type": "application/json"
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.invite) {
      document.getElementById('inviteCodeDisplay').innerHTML = "Ваш инвайт-код: " + data.invite;
    } else {
      alert("Ошибка генерации кода!");
    }
  });
};

document.addEventListener('DOMContentLoaded', function() {
  const burgerMenu = document.getElementById('burger-menu');
  const header = document.querySelector('.header');
  const burgerMenuBtn = document.querySelector('.burger-menu-btn');
  const iconsSrcElement = document.querySelector('.icons-src');

  burgerMenu.addEventListener('click', function (event) {
    // Останавливаем всплытие события, чтобы клик внутри меню не закрывал его
    event.stopPropagation();

    header.classList.toggle('open')
    burgerMenuBtn.classList.toggle('burger-menu-btn-open')

    
    if (iconsSrcElement.style.display == 'none') {
      iconsSrcElement.style.display = 'flex';
    } else {
        iconsSrcElement.style.display = 'none';
    } 
  });

  // Закрытие меню при клике вне его области
  document.addEventListener('click', function (event) {
    // Проверяем, открыто ли меню
    if (header.classList.contains('open')) {
      iconsSrcElement.style.display = 'none';
      // Проверяем, кликнули ли вне меню
      if (!header.contains(event.target) && !burgerMenu.contains(event.target)) {
        header.classList.remove('open');
        burgerMenuBtn.classList.remove('burger-menu-btn-open');
        iconsSrcElement.style.display = 'flex';
      }
    }
  });
});


const page = document.body.dataset.page;

if (page === "food") {
    
  
  const card = document.querySelector('.card');
  let isFlipped = false;
  let rotation = 0;

  card.addEventListener('click', () => {
    rotation += 180; // Увеличиваем угол поворота на 180 градусов
    card.style.transform = `rotateX(${rotation}deg)`;
    isFlipped = !isFlipped;
  });


} else if (page === "module") {





}
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
      if (data.invite_code) {
        document.getElementById('inviteCodeDisplay').innerHTML = "Ваш инвайт-код: " + data.invite_code;
      } else {
        alert("Ошибка генерации кода!");
      }
    });
  };

$(document).ready(function() {
  $("#id_username").on("input", function() {
      const UrlContainer = document.getElementById("url-containe")
      const MyUrl = UrlContainer.dataset.url;
    
      var username = $(this).val();
      if (username.length > 0) {
          $.ajax({
              url: MyUrl,
              type: "GET",
              data: {
                  'username': username
              },
              success: function(response) {
                  if (response.is_taken) {
                      $("#username-status").text("Логин занят").css("color", "red");
                  } else {
                      $("#username-status").text("Логин доступен").css("color", "green");
                  }
              }
          });
      } else {
          $("#username-status").text("");
      }
  });
});

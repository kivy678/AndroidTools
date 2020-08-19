$(document).ready(function($) {
  $('li[name=dbg-wait]').click(function() {
    $.ajax({
      url: "/app/wait",
      type: "GET",
      data: {"mode": $(this).text()},

      success: function(response) {
          console.log("SUCCESS: ");
      },
      error: function(error) {
          console.log("ERROR: " + error);
      }

    });
  });
});


$(document).ready(function($) {
  $('li[name=dynamic-menu]').click(function() {
    $.ajax({
      url: "/analysis/dynamic",
      type: "GET",
      data: {"menu": $(this).text()},

      success: function(response) {
          console.log("SUCCESS: ");
          $("#complate").html(response);
      },
      error: function(error) {
          console.log("ERROR: " + error);
      }

    });
  });
});

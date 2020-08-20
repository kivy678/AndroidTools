$(document).ready(function($) {
  $(".clickable-device-list").click(function() {
    var tr = $(this);
    var td = tr.children();

    var model = td.eq(0).text();

    $.ajax({
      url: "/dev/work",
      type: "GET",
      data: {"model": model},

      success: function(response) {
          console.log("SUCCESS: ");
          $("#device").html(response);
      },
      error: function(error) {
          console.log("ERROR: " + error);
      }

    });
  });
});


$(document).ready(function($) {
  $(".clickable-lib-list").click(function() {
    var tr = $(this);
    var td = tr.children();

    var lib = td.eq(0).text();

    $.ajax({
      url: "/analysis/static/format",
      type: "POST",
      data: {"lib": lib},

      success: function(response) {
          console.log("SUCCESS: ");
          $("#viewer").html(response);
      },
      error: function(error) {
          console.log("ERROR: " + error);
      }

    });
  });
});


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

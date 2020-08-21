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
  $(".clickable-pkg-list").click(function() {
    var tr = $(this);
    var td = tr.children();

    var fileName = td.eq(1).text();
    var pkg = td.eq(2).text();

    $.ajax({
      url: "/prefer/database/load",
      type: "POST",
      data: {'fileName': fileName, "pkg": pkg},

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
          $("#viewer").html(response);
      },
      error: function(error) {
          console.log("ERROR: " + error);
      }

    });
  });
});

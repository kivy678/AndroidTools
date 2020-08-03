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


$(document).ready(function(){
  $(".menu>a").click(function(){
    var submenu = $(this).next("ul");
    if( submenu.is(":visible") ){
      submenu.slideUp();
    }else{
      submenu.slideDown();
    }
    }).mouseover( function(){
      $(this).next("ul").slideDown();
  });
});


$(document).ready(function($) {
  $('li[name=dbg-wait]').click(function() {
    $.ajax({
      url: "/decomplie/wait",
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
  $('li[name=decomp-menu]').click(function() {
    $.ajax({
      url: "/decomplie/decomp",
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


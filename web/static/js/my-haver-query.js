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

$(function(){ // iffee function
  
    $(".dropdown-menu a").click(function(){ // dropdown menu for selecting a function
      
      $(".dropdown-btn:first-child").text($(this).text()); // change the first button text to this text
       $(".dropdown-btn:first-child").val($(this).text());
    });
  
  });


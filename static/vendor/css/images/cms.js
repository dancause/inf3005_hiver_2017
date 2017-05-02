$( function() {
    $( "#mydate" ).datepicker({ minDate: "-1Y", maxDate: "+1Y", 
    changeMonth: true,
    changeYear: true, 
    dateFormat: "yy-mm-dd"
    });
} );

$( function() {
    $( "#accordion" ).accordion({
      collapsible: true
    });
  } );
  
  
 $(document).ready(function(){            

         if ($.cookie('session')) { //if cookie isset
    var login=document.getElementById("login");
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          login.innerHTML = xhr.responseText;
        } else {console.log('Erreur avec le serveur');}} };
    xhr.open("GET", '/affichage_login/login', true);
    xhr.send();
  }
         }else{
         
    var login=document.getElementById("login");
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          login.innerHTML = xhr.responseText;
        } else {console.log('Erreur avec le serveur');}} };
    xhr.open("GET",'/affichage_login/logout' , true);
    xhr.send();
  }      
         
         
         
         
               
         }       


    });
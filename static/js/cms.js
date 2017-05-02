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
  
function functionurl() {
    var titre = document.getElementById("titre");
    var url_texte = document.getElementById("url");
   	var temp = titre.value.toLowerCase();
   	var temp2=''
 temp2=temp.normalize('NFD').replace(/[\u0300-\u036f]/g,"")
 temp2=temp2.replace(/[&\/\\#,+()$~%.'":*?<>{}'.<>^_=@&]/g, '');
  temp2 = temp2.split(' ').join('-');
  
  
  var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
	if (xhr.readyState === XMLHttpRequest.DONE) 
	{
        	if (xhr.status === 200) 
        	{
        	url_tag.innerHTML = xhr.responseText;
        	} 
        	else
        	{
        	console.log('Erreur avec le serveur');
        	}
	}  
};
xhr.open("GET", '/validation_url/'+temp2, true);
xhr.send();
  
}

function valider_url() {
    var url_texte = document.getElementById("url");
   	var temp = url_texte.value;
	console.log('temp '+ temp);
  var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
	if (xhr.readyState === XMLHttpRequest.DONE) 
	{
        	if (xhr.status === 200) 
        	{
        	url_tag.innerHTML = xhr.responseText;
        	} 
        	else
        	{
        	console.log('Erreur avec le serveur');
        	}
	}  
};
xhr.open("GET", '/verif_url/'+temp, true);
xhr.send();
  
}
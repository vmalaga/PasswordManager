// funcion para mostrar la contraseña
function cambiar(id, texto) {
		if (document.getElementById) {
			document.getElementById(id).innerHTML = texto.replace(/\&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
			document.getElementById(id).style.color = "black";
		}
}

(function($) {
	$(document).ready(function(){
		var windowWidth = 400
		var windowHeight = 300
		var centerWidth = (window.screen.width - windowWidth) / 2;
		var centerHeight = (window.screen.height - windowHeight) / 2;
		
		   
		   $('.newWindow').click(function (event){
		   	var url = $(this).attr("href");
		   	var windowName = "popUp";//$(this).attr("name");
		
		window.open(url, windowName, 'resizable=0,width=' + windowWidth + 
        ',height=' + windowHeight + 
        ',left=' + centerWidth + 
        ',top=' + centerHeight);
		event.preventDefault();
 
        });
	});
})(django.jQuery);
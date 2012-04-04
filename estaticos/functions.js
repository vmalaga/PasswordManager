// funcion para mostrar la contraseña
function cambiar(id, texto) {
		if (document.getElementById) {
			document.getElementById(id).innerHTML = texto.replace(/\&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
			document.getElementById(id).style.color = "black";
		}
}

var windowSizeArray = [ "width=200,height=200", "width=300,height=400,scrollbars=yes" ];
$(document).ready(function(){
	$('.newWindow').click(function (event){
		var url = $(this).attr("href");
		var windowName = "popUp";//$(this).attr("name");
		var windowSize = windowSizeArray[$(this).attr("rel")];
		
		window.open(url, windowName, windowSize);
		event.preventDefault();
 
        });
});


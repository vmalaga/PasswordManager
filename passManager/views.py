from django.http import HttpResponse
from passManager.models import passDb, passEncr

def send_email(request, idrow):
    row = passDb.objects.get(pk=idrow)
    name = row.name
#    print name
    html = "<html><body>HOLA MUNDO %s </body></html>" % name
    response = HttpResponse(html)
    return response


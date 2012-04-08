from django.http import HttpResponseRedirect
from django.http import HttpResponse
from passManager.models import passDb, passEncr
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import User
from django.forms import CharField
from django.template import RequestContext



class ContactForm(forms.Form):
    mailto = forms.EmailField()
    
class pruebaForm(forms.ModelForm):
    mailto = forms.EmailField()
    class Meta:
        model = passDb
        exclude = ('name','login','server','uploader','notes','password',)
        
def pruebaView(request, rowid):
        row = passDb.objects.get(pk=int(rowid))
        form = pruebaForm(instance=row)
        name, login, server = (row.name, row.login, row.server)
        print name + login + server
        return render_to_response('pruebaview.html', {
        'form': form,
        })
    

def thanks(request):
    html = "Su mensaje a sido enviado con exito"
    return HttpResponse(html)


def sendEmailView(request, idrow):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mailto = [form.cleaned_data['mailto'],]
            name = request.POST['name']
            login = request.POST['login']
            server = request.POST['server']
            fromemail = "passmanager@lnxnet.es"
            notes = request.POST['notes']
            password = request.POST['password']
            subject = "Password - " + name
            message = """<p><strong>name:</strong> %s<br>
                         <p><strong>login:</strong> %s<br>
                         <p><strong>server:</strong> %s<br>
                         <p><strong>notes:</strong> %s<br>
                         <p><strong>password:</strong> %s""" % (name, login, server, notes, password)
            
            from django.core.mail import EmailMessage
            msg = EmailMessage(subject, message, fromemail, mailto)
            msg.content_subtype = "html"
            msg.send()
            return HttpResponseRedirect('/thanks/')
        else:
            return HttpResponse(form.errors['mailto'])
    else:
        row = passDb.objects.get(pk=int(idrow))
        name = row.name
        login = row.login
        server = row.server
        autor = row.uploader
        notes = row.notes
        fromemail = (User.objects.get(username=autor)).email
        password = passEncr('decrypt', row.password)
        
        form = ContactForm() # An unbound form
        return render_to_response('send_email.html', {
        'form': form,
        'name': name,
        'login': login,
        'server': server,
        'autor': autor,
        'notes': notes,
        'fromemail': fromemail,
        'password': password,
        }, 
                                  context_instance=RequestContext(request))

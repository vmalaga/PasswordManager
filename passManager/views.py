from django.http import HttpResponseRedirect
from django.http import HttpResponse
from passManager.models import passDb, passEncr
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import User
from django.forms import CharField
from django.template import RequestContext
from django.forms import TextInput, Textarea, PasswordInput, HiddenInput
from django.conf import settings

class ContactPassForm(forms.ModelForm):
    mailto = forms.EmailField(label='Destinatario')
    class Meta:
        model = passDb
#        exclude = ('uploader',)
        widgets = {
            'name': TextInput(attrs={'readonly':'readonly','size':'60'}),
            'login': TextInput(attrs={'readonly':'readonly','size':'60'}),
            'password': PasswordInput(render_value=True),
            'server': TextInput(attrs={'readonly':'readonly','size':'60'}),
            'notes': Textarea(attrs={'readonly':'readonly'}),
            'uploader': HiddenInput(),
            }
        
def mailsent(request):
    return render_to_response('mailsent.html', context_instance=RequestContext(request))


def sendPassEmailView(request, rowid):
    from django.core.mail import EmailMultiAlternatives
    if request.method == 'POST':
        form = ContactPassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            server = form.cleaned_data['server']
            notes = form.cleaned_data['notes']
            mailto = form.cleaned_data['mailto']
            sender = settings.PASS_MANAGER_EMAIL_FROM
            
            subject = "%s - %s" % (settings.PASS_MANAGER_EMAIL_SUBJECT, name)
            text_message ="""Django-PassManager
            Name: %s
            Login: %s
            Password: %s
            Server: %s
            Notes: %s""" % (name, login, password, server, notes)
            
            html_message = """<h2>%s</h2>
            <p><strong>Name: </strong> %s</p>
            <p><strong>Login: </strong> %s</p>
            <p><strong>Password: </strong> %s</p>
            <p><strong>Server: </strong> %s</p>
            <p><strong>Notes: </strong> %s</p>""" \
% (settings.PASS_MANAGER_EMAIL_TITLE, name, login, password, server, notes)
            
            msg = EmailMultiAlternatives(subject, text_message, sender, [mailto])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            return HttpResponseRedirect('/mailsent/')
    else:
        row = passDb.objects.get(pk=int(rowid))
        row.password = passEncr('decrypt', row.password)
        form = ContactPassForm(instance=row)
        
        
    return render_to_response('send_pass.html', {'form': form} ,
                              context_instance=RequestContext(request))

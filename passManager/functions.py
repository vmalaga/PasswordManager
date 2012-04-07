'''
Created on 04/04/2012

@author: vmalaga
'''

def passEncr(action, text):
    # Funcion para encriptar de desencriptar las passwords
    # action = encryt or action = decrypt
    # basado en el modulo django.core.signing
    from django.core import signing
    if action == "encrypt":
        return signing.dumps(text)
    
    if action == "decrypt":
        return signing.loads(text)
    
def send_invite(self, request, queryset):
    from django.core.mail import send_mail
    # the below can be modified according to your application.
    # queryset will hold the instances of your model
    for profile in queryset:
        send_mail(subject="Invite", message="Hello", from_eamil='passManager@lnxnet.es', recipient_list=[profile.email])
    send_invite.short_description = "Send invitation"
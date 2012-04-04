'''
Created on 04/04/2012

@author: vmalaga
'''
from Crypto.Cipher import AES
import base64
import settings

def passEncr(action, text):
    # Funcion para encriptar de desencriptar las passwords
    # action = encryt or action = decrypt
    BLOCK_SIZE = 32
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    secret = settings.SECRET_KEY
    cipher = AES.new(secret)
    if action == "encrypt":
        return EncodeAES(cipher, text)
    
    if action == "decrypt":
        return DecodeAES(cipher, text)
    
def send_invite(self, request, queryset):
    from django.core.mail import send_mail
    # the below can be modified according to your application.
    # queryset will hold the instances of your model
    for profile in queryset:
        send_mail(subject="Invite", message="Hello", from_eamil='passManager@lnxnet.es', recipient_list=[profile.email])
    send_invite.short_description = "Send invitation"
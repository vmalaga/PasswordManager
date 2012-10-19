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
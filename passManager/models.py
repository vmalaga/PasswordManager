from django.contrib.auth.models import User
from django.db import models
from passManager.functions import passEncr

class passDb(models.Model):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    server = models.CharField(max_length=60)
    date = models.DateField(auto_now=True)
    uploader = models.ForeignKey(User)
    notes = models.TextField()
 
    def __unicode__(self):
        return self.name
    
    def getClickMe(self):
        password = passEncr('decrypt', self.password)
        idrow = self.id
        return '<font color="red"><span id=\"%s\" onClick=\"cambiar(\'%s\',\'%s\');\">ClickME</span></font>' % (idrow, idrow, password)
    getClickMe.allow_tags = True
    getClickMe.short_description = "Password"
    
    def showPass(self):
        if len(self.password) != 0:
            password = passEncr('decrypt', self.password)
        else:
            password = ""
        return password
    


    

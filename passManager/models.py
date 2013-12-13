from django.contrib.auth.models import User
from django.db import models
from passManager.functions import passEncr
import time
import pytz
import datetime

class passDb(models.Model):
    class Meta:
        verbose_name = 'Password'
        
    deprecated = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    server = models.CharField(max_length=60)
    uploader = models.ForeignKey(User)
    notes = models.TextField(null=True, blank=True, default = "")
    creation_date = models.DateTimeField(editable=False)
    modification_date = models.DateTimeField(auto_now=True, null=True,
            blank=True)
    valid_since_date = models.DateTimeField(null=True, blank=True, default = None)
    valid_until_date = models.DateTimeField(null=True, blank=True, default = None)

    def __unicode__(self):
        return self.name
    
    def getClickMe(self):
        password = passEncr('decrypt', self.password)
        idrow = self.id
        return '<font color="red"><span id=\"%s\" onClick=\"cambiar(\'%s\',\'%s\');\">ClickME</span></font>' % (idrow, idrow, password)
    getClickMe.allow_tags = True
    getClickMe.short_description = "Password"
    
    def _get_password(self):
        if len(self.password) != 0:
            password = passEncr('decrypt', self.password)
        else:
            password = ""
        return password
    

    def save(self, *args, **kwargs):

        d = datetime.datetime.fromtimestamp(time.time(), pytz.UTC)
        if not self.creation_date:
            self.creation_date = d
        if self.valid_until_date and self.valid_until_date < d:
            self.deprecated = True
        super(passDb, self).save(*args, **kwargs)

    

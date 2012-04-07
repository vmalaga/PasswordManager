from django.contrib import admin
from passManager.models import passDb, passEncr


class passManagerAdmin(admin.ModelAdmin):
    class Media:
        js = ("/static/functions.js",)
    
    actions = ['export_as_json']    
    actions_on_bottom = True
    actions_on_top = False
    list_display = ('name','login','getClickMe','server','uploader','date','notes','send_email_html')
    list_filter = ('login','server','uploader','date')
    #ordering = ['date']
    fieldsets = [
                 (None,         {'fields': ['name',('login','password'),'server','notes']}),
                 #('Notas',         {'fields': ['uploader'], 'classes': ['collapse']}),
                 ]
    search_fields = ['name','login','server','notes']
        
    def save_model(self, request, obj, form, change):
        obj.password = passEncr('encrypt', obj.password)
        obj.uploader = request.user
        obj.nivel = 1
        obj.save()
        

    def send_email_html(self, queryset):
        return '<center><a href="/send_email/%s" rel="0" class="newWindow"><img src="/static/Email_icon.gif"></img></a></center>' % queryset.id
    send_email_html.short_description = 'Email'
    send_email_html.allow_tags = True
    
        
    def export_as_json(self, request, queryset):
        from django.http import HttpResponse
        from django.core import serializers
        response = HttpResponse(mimetype="text/javascript")
        serializers.serialize("json", queryset, stream=response)
        return response

        
admin.site.register(passDb, passManagerAdmin)

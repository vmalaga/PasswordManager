from django.contrib import admin
from passManager.models import passDb, passEncr
from django.contrib.admin import SimpleListFilter


class loginsFilter(SimpleListFilter):
    ''' Filtro para el admin basado en los
    logins. Se hace facetado de los resultados
    y solo muestra aquellos logins que tienen
    mas de 1 aparicion'''
    title = "TOP Logins"
    parameter_name = "logins"
    # Get all objects
    rows = passDb.objects.all()                                                                                                                                                      
    # Logins list                                                                                                                                                     
    logins = []                                                                                                                                                                      
    for row in rows:
        logins.append(row.login)                                                                                                                                                     
    # Duplicate clean
    logins = set(logins)                                                                                                                                                             
    
    # Get tuple with login and ocurences
    lista = {}
    for l in set(logins):
        numrows = passDb.objects.filter(login=l).count()                                                                                                                                      
        if numrows > 2:
            lista[str(l)] = numrows                                                                                                                                                  
                                                                                                                                                                                 
    # Import module for order dictionary                                                                                                                                                
    from operator import itemgetter                                                                                                                                                  
    slist = sorted(lista.items(), key=itemgetter(1), reverse=True)                                                                                                                   
    
    # Generate facetes
    facet = []                                                                                                                                                                       
    for n in range(0 ,(len(slist))):
        facet.append(((slist[n][0]),(slist[n][0]+' ('+str(slist[n][1]))+')'))
    
    def lookups(self, request, model_admin):
        return (
                self.facet
#                ('roots', u"roots"),
#                ('admins', u"admins"),
                )
        
    def queryset(self, request, queryset):
        for n in range(0 ,(len(self.slist))):
            val = self.slist[n][0]
            if self.value() == val:
                return queryset.filter(login=val)


class passManagerAdmin(admin.ModelAdmin):
    class Media:
        js = ("jquery-1.7.1.min.js", "jquery-ui-1.8.18.custom.min.js", "functions.js",)
        css = {
            "all": ("jquery-ui-1.8.18.custom.css",)
        }

    ordering = ['modification_date']

    list_per_page = 30
    actions = ['export_as_json']
    actions_on_bottom = True
    actions_on_top = False
    list_display_links = ['name']
    list_display = \
      ('name','login','getClickMe','server','uploader','creation_date','notes','send_email_html')
    list_editable = []
    readonly_fields = [
        'creation_date',
        "uploader",
        "deprecated"
    ]

    list_filter = (loginsFilter,'uploader','creation_date')
    fieldsets = [
		    (None,         {'fields': ['name',('login','password'),'server','notes']}),
		    ]

    search_fields = ['name','login','server','notes']
        
    def save_model(self, request, obj, form, change):
        #obj.password = passEncr('encrypt', obj.password)
        obj.uploader = request.user
        obj.nivel = 1
        obj.save()
    
    def send_email_html(self, queryset):
        buttons = """                                                                                                                                                            
            <div style="width:20px">                                                                                                                                             
            <a href="/send_pass/%s" title="Enviar por Email" name="Envio de Correo" class="mailwindow"><img src="/static/mail-message-new.png"></img></a>                       
            </div>
        """ % (queryset.id)
        return buttons
    send_email_html.short_description = ''
    send_email_html.allow_tags = True
    
    def export_as_json(self, request, queryset):
        from django.http import HttpResponse
        from django.core import serializers
        response = HttpResponse(mimetype="text/javascript")
        serializers.serialize("json", queryset, stream=response)
        return response

        
admin.site.register(passDb, passManagerAdmin)

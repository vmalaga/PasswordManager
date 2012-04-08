from django.contrib import admin
from passManager.models import passDb, passEncr
from django.contrib.admin import SimpleListFilter


class loginsFilter(SimpleListFilter):
    ''' Filtro para el admin basado en los
    logins. Se hace facetado de los resultados
    y solo muestra aquellos logins que tienen
    mas de 1 aparicion'''
    title = "Logins"
    parameter_name = "logins"
    rows = passDb.objects.all()
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
        filterlogins = passDb.objects.filter(login=l)                                                                                                                                      
        numrows = len(filterlogins)
        # View only logins with more than 1                                                                                                                                                        
        if numrows > 1:
            lista[str(l)] = numrows                                                                                                                                                  
                                                                                                                                                                                 
    # Import module for order dictionary                                                                                                                                                
    from operator import itemgetter                                                                                                                                                  
    #print sorted(lista.items(), key=itemgetter(1), reverse=True)                                                                                                                     
    slist = sorted(lista.items(), key=itemgetter(1), reverse=True)                                                                                                                   
    
    # Generate facetes
    facet = []                                                                                                                                                                       
    for n in range(0 ,(len(slist))):
        #print (slist[n][0]),(slist[n][0]+'('+str(slist[n][1]))+')'                                                                                                                   
        facet.append(((slist[n][0]),(slist[n][0]+'('+str(slist[n][1]))+')'))
    
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
        js = ("/static/functions.js",)
    
    list_per_page = 20
    actions = ['export_as_json']    
    actions_on_bottom = True
    actions_on_top = False
    list_display = ('name','login','getClickMe','server','uploader','date','notes','send_email_html')
#    list_filter = ('login','server','uploader','date')
    list_filter = (loginsFilter,'uploader','date')
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
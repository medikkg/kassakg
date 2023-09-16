from django.contrib import admin
from .models import Service, Client, ClientAddress, Task, Lead

class LeadAdmin(admin.ModelAdmin):
    list_display = ['pk', 'client_info', 'work_start', 'lead_status']
    list_filter = ('lead_status',)

admin.site.register(ClientAddress)
admin.site.register(Client)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Service)

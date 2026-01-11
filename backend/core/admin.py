from django.contrib import admin
from .models import Location, Patient, Referral, CommunicationLog, AuditLog

admin.site.register(Location)
admin.site.register(Patient)
admin.site.register(Referral)
admin.site.register(CommunicationLog)
admin.site.register(AuditLog)

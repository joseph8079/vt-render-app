from django.contrib import admin
from .models import TherapistProfile, SlotTemplate, SlotAssignment

admin.site.register(TherapistProfile)
admin.site.register(SlotTemplate)
admin.site.register(SlotAssignment)

from django.contrib import admin
from .models import ClinicalReview, Program, ProgramGoal, ProgramSession, NoteTemplate, TherapyNote, GoalProgressEntry

admin.site.register(ClinicalReview)
admin.site.register(Program)
admin.site.register(ProgramGoal)
admin.site.register(ProgramSession)
admin.site.register(NoteTemplate)
admin.site.register(TherapyNote)
admin.site.register(GoalProgressEntry)

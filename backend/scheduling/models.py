from django.db import models
from django.contrib.auth.models import User
from core.models import Location
from therapy.models import Program, ProgramSession
from therapy.services import DOW, generate_sessions
from django.utils import timezone

class TherapistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="therapist_profile")
    gender = models.CharField(max_length=1, choices=[("M","Male"),("F","Female")], default="M")
    is_therapist = models.BooleanField(default=True)
    def __str__(self): return self.user.username

class SlotTemplate(models.Model):
    DAYS = [("MON","Mon"),("TUE","Tue"),("WED","Wed"),("THU","Thu"),("FRI","Fri"),("SAT","Sat"),("SUN","Sun")]
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    therapist = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist_gender = models.CharField(max_length=1, choices=[("M","Male"),("F","Female")])
    patient_gender_allowed = models.CharField(max_length=1, choices=[("M","Male"),("F","Female"),("A","Any")], default="A")
    day1 = models.CharField(max_length=3, choices=DAYS)
    day2 = models.CharField(max_length=3, choices=DAYS)
    time_start = models.TimeField()
    session_minutes = models.PositiveSmallIntegerField(default=30)
    room = models.CharField(max_length=50, blank=True, default="")
    is_active = models.BooleanField(default=True)

class SlotAssignment(models.Model):
    slot_template = models.ForeignKey(SlotTemplate, on_delete=models.CASCADE, related_name="assignments")
    program = models.OneToOneField(Program, on_delete=models.CASCADE, related_name="slot_assignment")
    status = models.CharField(max_length=20, default="ASSIGNED")  # HELD/ASSIGNED
    held_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_program_sessions(self, start_date):
        slot = self.slot_template
        days_pair = (DOW[slot.day1], DOW[slot.day2])
        sessions = generate_sessions(start_date, slot.time_start, slot.session_minutes, days_pair, total_sessions=self.program.total_sessions)
        self.program.sessions.all().delete()
        objs = []
        for i, (s,e) in enumerate(sessions, start=1):
            objs.append(ProgramSession(program=self.program, session_number=i, planned_start=s, planned_end=e, therapist=slot.therapist, status="SCHEDULED"))
        ProgramSession.objects.bulk_create(objs)
        self.program.start_date = start_date
        self.program.status = "ACTIVE"
        self.program.save(update_fields=["start_date","status"])

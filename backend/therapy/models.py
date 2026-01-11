from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Referral, Patient

class ClinicalReview(models.Model):
    class Decision(models.TextChoices):
        NEEDS_VT = "NEEDS_VT", "Needs VT"
        NO_VT = "NO_VT", "No VT"
        MORE_INFO = "MORE_INFO", "More Info"

    referral = models.OneToOneField(Referral, on_delete=models.CASCADE, related_name="clinical_review")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    decision = models.CharField(max_length=20, choices=Decision.choices, default=Decision.NEEDS_VT)
    summary = models.TextField(blank=True, default="")
    recommended_frequency_per_week = models.PositiveSmallIntegerField(default=2)
    recommended_total_sessions = models.PositiveSmallIntegerField(default=22)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Program(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="programs")
    referral = models.OneToOneField(Referral, on_delete=models.SET_NULL, null=True, blank=True, related_name="program")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    total_sessions = models.PositiveSmallIntegerField(default=22)
    sessions_per_week = models.PositiveSmallIntegerField(default=2)
    session_minutes = models.PositiveSmallIntegerField(default=30)
    status = models.CharField(max_length=30, default="PLANNED")  # PLANNED/ACTIVE/COMPLETED/ON_HOLD/DROPPED
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

class ProgramGoal(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=80, blank=True, default="")
    baseline = models.CharField(max_length=80, blank=True, default="")
    target = models.CharField(max_length=80, blank=True, default="")
    current_progress = models.PositiveSmallIntegerField(default=0)  # 0-4
    is_active = models.BooleanField(default=True)

class ProgramSession(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="sessions")
    session_number = models.PositiveSmallIntegerField()
    planned_start = models.DateTimeField(null=True, blank=True)
    planned_end = models.DateTimeField(null=True, blank=True)
    therapist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=30, default="PLANNED")  # PLANNED/SCHEDULED/COMPLETED/CANCELLED/NO_SHOW
    symptom_score = models.PositiveSmallIntegerField(null=True, blank=True)      # 0-10
    engagement_score = models.PositiveSmallIntegerField(null=True, blank=True)   # 1-5
    homework_compliance = models.PositiveSmallIntegerField(null=True, blank=True) # 0-100
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("program","session_number")
        ordering = ("session_number",)

class NoteTemplate(models.Model):
    name = models.CharField(max_length=120)
    kind = models.CharField(max_length=40, default="SESSION")  # SESSION/REASSESS/DISCHARGE
    schema = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

class TherapyNote(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="therapy_notes")
    session = models.ForeignKey(ProgramSession, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    therapist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    template = models.ForeignKey(NoteTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=40, default="SESSION")
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GoalProgressEntry(models.Model):
    goal = models.ForeignKey(ProgramGoal, on_delete=models.CASCADE, related_name="progress_entries")
    session = models.ForeignKey(ProgramSession, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.PositiveSmallIntegerField(default=0)  # 0-4
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

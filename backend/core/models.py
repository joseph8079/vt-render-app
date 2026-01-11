from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.name

class Patient(models.Model):
    GENDER_CHOICES = [("M","Male"),("F","Female"),("U","Unknown")]
    mrn = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="U")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    parent_name = models.CharField(max_length=120, blank=True, default="")
    parent_phone = models.CharField(max_length=50, blank=True, default="")
    parent_email = models.EmailField(blank=True, default="")
    preferred_language = models.CharField(max_length=50, blank=True, default="")
    insurance = models.CharField(max_length=120, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.last_name}, {self.first_name} ({self.mrn})"

class Referral(models.Model):
    class Status(models.TextChoices):
        FLAGGED = "FLAGGED", "Flagged by Provider"
        INTAKE_CREATED = "INTAKE_CREATED", "Intake Created"
        REVIEW_PENDING = "REVIEW_PENDING", "Review Pending"
        REVIEW_COMPLETED = "REVIEW_COMPLETED", "Review Completed"
        PLAN_READY = "PLAN_READY", "Plan Ready"
        PARENT_CONTACTED = "PARENT_CONTACTED", "Parent Contacted"
        PARENT_CONFIRMED = "PARENT_CONFIRMED", "Parent Confirmed"
        SLOT_ASSIGNED = "SLOT_ASSIGNED", "Slot Assigned"
        SCHEDULED_INTERNAL = "SCHEDULED_INTERNAL", "Scheduled (Internal)"
        ACTIVE_THERAPY = "ACTIVE_THERAPY", "Active Therapy"
        ON_HOLD = "ON_HOLD", "On Hold"
        COMPLETED = "COMPLETED", "Completed"
        DROPPED = "DROPPED", "Dropped / Not Candidate"

    STATUS_ORDER = [
        Status.FLAGGED, Status.INTAKE_CREATED, Status.REVIEW_PENDING, Status.REVIEW_COMPLETED,
        Status.PLAN_READY, Status.PARENT_CONTACTED, Status.PARENT_CONFIRMED, Status.SLOT_ASSIGNED,
        Status.SCHEDULED_INTERNAL, Status.ACTIVE_THERAPY, Status.ON_HOLD, Status.COMPLETED, Status.DROPPED
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="referrals")
    referring_provider = models.CharField(max_length=120, blank=True, default="")
    visit_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=40, choices=Status.choices, default=Status.FLAGGED)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="vt_referrals_owned")

    priority = models.CharField(max_length=20, blank=True, default="Normal")
    due_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_transition_to(self, new_status: str) -> bool:
        try:
            return self.STATUS_ORDER.index(new_status) >= self.STATUS_ORDER.index(self.status)
        except ValueError:
            return False

class CommunicationLog(models.Model):
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE, related_name="communications")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=30, default="CALL")  # CALL/SMS/EMAIL
    outcome = models.CharField(max_length=60, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    entity = models.CharField(max_length=60)
    entity_id = models.CharField(max_length=64)
    action = models.CharField(max_length=60)
    before = models.JSONField(null=True, blank=True)
    after = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

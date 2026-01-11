from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta, time
import random

from core.models import Location, Patient, Referral
from therapy.models import NoteTemplate
from scheduling.models import TherapistProfile, SlotTemplate

DEFAULT_SESSION_TEMPLATE = {
  "sections": [
    {"title":"Session","fields":[
      {"key":"activities","label":"Activities","type":"multiselect","options":["Saccades","Pursuits","Vergence","Accommodation","VMI"],"required":False},
      {"key":"symptom_score","label":"Symptom score (0-10)","type":"number","min":0,"max":10,"required":False},
      {"key":"engagement","label":"Engagement (1-5)","type":"number","min":1,"max":5,"required":False},
      {"key":"homework_compliance","label":"Homework compliance %","type":"number","min":0,"max":100,"required":False},
      {"key":"narrative","label":"Narrative","type":"text","required":False}
    ]}
  ]
}

class Command(BaseCommand):
    help = "Seed demo data for local testing"

    def handle(self, *args, **options):
        locs = {n: Location.objects.get_or_create(name=n)[0] for n in ["Williamsburg","Boro Park","Monroe"]}

        # Staff accounts
        for uname in ["vt_manager","intake","reviewer"]:
            u, created = User.objects.get_or_create(username=uname, defaults={"is_staff": True})
            if created:
                u.set_password("password"); u.save()

        # Therapists
        for uname, gender in [("therapist_m1","M"),("therapist_f1","F")]:
            u, created = User.objects.get_or_create(username=uname, defaults={"is_staff": False})
            if created:
                u.set_password("password"); u.save()
            TherapistProfile.objects.get_or_create(user=u, defaults={"gender": gender, "is_therapist": True})

        NoteTemplate.objects.get_or_create(
            name="Default Session Note",
            kind="SESSION",
            defaults={"schema": DEFAULT_SESSION_TEMPLATE, "is_active": True}
        )

        # Slot templates (recurring pairs)
        SlotTemplate.objects.get_or_create(
            location=locs["Williamsburg"],
            therapist=User.objects.get(username="therapist_m1"),
            therapist_gender="M",
            patient_gender_allowed="M",
            day1="MON", day2="THU",
            time_start=time(16,0),
            defaults={"session_minutes": 30, "room": "1", "is_active": True}
        )
        SlotTemplate.objects.get_or_create(
            location=locs["Williamsburg"],
            therapist=User.objects.get(username="therapist_f1"),
            therapist_gender="F",
            patient_gender_allowed="F",
            day1="TUE", day2="FRI",
            time_start=time(16,30),
            defaults={"session_minutes": 30, "room": "2", "is_active": True}
        )

        # Patients + referrals
        for i in range(10):
            p, _ = Patient.objects.get_or_create(
                mrn=f"MRN{i+1000}",
                defaults={
                    "first_name": f"Kid{i+1}",
                    "last_name": "Patient",
                    "gender": random.choice(["M","F"]),
                    "location": random.choice(list(locs.values())),
                    "parent_name": "Parent",
                    "parent_phone": "555-555-5555",
                    "insurance": "Insurance",
                }
            )
            Referral.objects.get_or_create(
                patient=p,
                defaults={
                    "referring_provider": "Dr. Provider",
                    "visit_date": date.today() - timedelta(days=random.randint(0,21)),
                    "status": random.choice([Referral.Status.FLAGGED, Referral.Status.REVIEW_PENDING, Referral.Status.PLAN_READY]),
                }
            )

        self.stdout.write(self.style.SUCCESS("Seeded demo data. Users: vt_manager/intake/reviewer/therapist_m1/therapist_f1 (password: password)"))

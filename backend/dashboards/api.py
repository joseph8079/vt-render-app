from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg, Q

from core.models import Referral
from therapy.models import Program, ProgramSession

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        last_30 = now - timedelta(days=30)
        next_7 = now + timedelta(days=7)

        referrals_30 = Referral.objects.filter(created_at__gte=last_30).count()
        active_programs = Program.objects.filter(status="ACTIVE").count()

        funnel = Referral.objects.values("status").annotate(c=Count("id"))
        funnel_map = {x["status"]: x["c"] for x in funnel}

        upcoming = ProgramSession.objects.filter(planned_start__gte=now, planned_start__lte=next_7, status="SCHEDULED").count()

        completed = ProgramSession.objects.filter(planned_start__gte=last_30, status="COMPLETED")
        outcome = completed.aggregate(
            avg_symptom=Avg("symptom_score"),
            avg_engagement=Avg("engagement_score"),
            avg_homework=Avg("homework_compliance"),
        )

        at_risk = Program.objects.filter(status="ACTIVE").annotate(
            s7=Count("sessions", filter=Q(sessions__planned_start__gte=now, sessions__planned_start__lte=next_7, sessions__status="SCHEDULED"))
        ).filter(s7__lt=2).values("id","patient_id","s7")[:200]

        return Response({
            "referrals_last_30_days": referrals_30,
            "active_programs": active_programs,
            "funnel": funnel_map,
            "upcoming_scheduled_sessions_next_7_days": upcoming,
            "outcomes_last_30_days": outcome,
            "at_risk_programs_next_7_days": list(at_risk),
        })

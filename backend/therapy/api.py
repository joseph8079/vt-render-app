from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import time

from .models import ClinicalReview, Program, ProgramGoal, ProgramSession, NoteTemplate, TherapyNote, GoalProgressEntry
from .serializers import ClinicalReviewSerializer, ProgramSerializer, ProgramGoalSerializer, TherapyNoteSerializer, NoteTemplateSerializer
from .services import generate_sessions, DOW

class ClinicalReviewViewSet(viewsets.ModelViewSet):
    queryset = ClinicalReview.objects.select_related("referral","reviewer").all().order_by("-updated_at")
    serializer_class = ClinicalReviewSerializer
    permission_classes = [IsAuthenticated]

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all().order_by("-created_at")
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        patient = self.request.query_params.get("patient")
        if patient:
            qs = qs.filter(patient_id=patient)
        return qs

    @action(detail=True, methods=["post"])
    def add_goal(self, request, pk=None):
        program = self.get_object()
        ser = ProgramGoalSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        goal = ProgramGoal.objects.create(program=program, **ser.validated_data)
        return Response(ProgramGoalSerializer(goal).data, status=201)

    @action(detail=True, methods=["post"])
    def set_goal_progress(self, request, pk=None):
        program = self.get_object()
        goal_id = request.data.get("goal_id")
        session_id = request.data.get("session_id")
        value = int(request.data.get("value", 0))
        goal = ProgramGoal.objects.get(id=goal_id, program=program)
        goal.current_progress = value
        goal.save(update_fields=["current_progress"])
        GoalProgressEntry.objects.create(goal=goal, session_id=session_id, value=value, created_by=request.user)
        return Response({"ok": True})

    @action(detail=True, methods=["post"])
    def generate_22(self, request, pk=None):
        program = self.get_object()
        start_date = request.data.get("start_date")
        time_start = request.data.get("time_start","16:00")
        days_pair = request.data.get("days_pair", ["MON","THU"])
        therapist_id = request.data.get("therapist_id")

        if not start_date:
            return Response({"detail":"start_date required (YYYY-MM-DD)"}, status=400)

        sd = timezone.datetime.fromisoformat(start_date).date()
        hh, mm = [int(x) for x in time_start.split(":")]
        t0 = time(hh, mm)
        wds = tuple(DOW[d] for d in days_pair)

        sessions = generate_sessions(sd, t0, program.session_minutes, wds, total_sessions=program.total_sessions)

        program.sessions.all().delete()
        objs = []
        for i, (s,e) in enumerate(sessions, start=1):
            objs.append(ProgramSession(program=program, session_number=i, planned_start=s, planned_end=e, therapist_id=therapist_id, status="SCHEDULED"))
        ProgramSession.objects.bulk_create(objs)

        program.start_date = sd
        program.status = "ACTIVE"
        program.save(update_fields=["start_date","status"])
        return Response(ProgramSerializer(program).data)

class NoteTemplateViewSet(viewsets.ModelViewSet):
    queryset = NoteTemplate.objects.all().order_by("kind","name")
    serializer_class = NoteTemplateSerializer
    permission_classes = [IsAuthenticated]

class TherapyNoteViewSet(viewsets.ModelViewSet):
    queryset = TherapyNote.objects.select_related("therapist").all().order_by("-updated_at")
    serializer_class = TherapyNoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(therapist=self.request.user)

    @action(detail=False, methods=["get"])
    def by_program(self, request):
        program_id = request.query_params.get("program_id")
        qs = self.queryset.filter(program_id=program_id)
        return Response(self.get_serializer(qs, many=True).data)

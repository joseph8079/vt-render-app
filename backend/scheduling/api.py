from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import SlotTemplate, SlotAssignment
from .serializers import SlotTemplateSerializer, SlotAssignmentSerializer
from therapy.models import Program

class SlotTemplateViewSet(viewsets.ModelViewSet):
    queryset = SlotTemplate.objects.select_related("location","therapist").all().order_by("-id")
    serializer_class = SlotTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        location_id = self.request.query_params.get("location_id")
        patient_gender = self.request.query_params.get("patient_gender")
        if location_id:
            qs = qs.filter(location_id=location_id)
        if patient_gender in ("M","F"):
            qs = qs.filter(patient_gender_allowed__in=["A", patient_gender])
        return qs

class SlotAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SlotAssignment.objects.select_related("slot_template","program").all().order_by("-created_at")
    serializer_class = SlotAssignmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def assign_and_generate(self, request):
        program_id = request.data.get("program_id")
        slot_template_id = request.data.get("slot_template_id")
        start_date = request.data.get("start_date")
        if not all([program_id, slot_template_id, start_date]):
            return Response({"detail":"program_id, slot_template_id, start_date required"}, status=400)

        program = Program.objects.get(id=program_id)
        SlotAssignment.objects.filter(program=program).delete()
        assignment = SlotAssignment.objects.create(program=program, slot_template_id=slot_template_id, status="ASSIGNED")

        sd = timezone.datetime.fromisoformat(start_date).date()
        assignment.generate_program_sessions(sd)

        # If referral linked, reflect status
        if program.referral_id:
            ref = program.referral
            ref.status = "SLOT_ASSIGNED"
            ref.save(update_fields=["status","updated_at"])

        return Response(SlotAssignmentSerializer(assignment).data, status=201)

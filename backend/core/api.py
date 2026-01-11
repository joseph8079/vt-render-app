from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Patient, Referral, CommunicationLog, AuditLog
from .serializers import PatientSerializer, ReferralSerializer, CommunicationLogSerializer, UserLiteSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related("location").all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        if q:
            return qs.filter(mrn__icontains=q) | qs.filter(first_name__icontains=q) | qs.filter(last_name__icontains=q)
        return qs

class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.select_related("patient","owner","patient__location").all().order_by("-updated_at")
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        before = ReferralSerializer(self.get_object()).data
        obj = serializer.save()
        after = ReferralSerializer(obj).data
        AuditLog.objects.create(actor=self.request.user, entity="Referral", entity_id=str(obj.id), action="UPDATE", before=before, after=after)

    @action(detail=True, methods=["post"])
    def add_communication(self, request, pk=None):
        referral = self.get_object()
        ser = CommunicationLogSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        comm = CommunicationLog.objects.create(
            referral=referral,
            created_by=request.user,
            kind=ser.validated_data.get("kind","CALL"),
            outcome=ser.validated_data.get("outcome",""),
            notes=ser.validated_data.get("notes",""),
        )
        return Response(CommunicationLogSerializer(comm).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def transition(self, request, pk=None):
        referral = self.get_object()
        new_status = request.data.get("status")
        override = bool(request.data.get("override", False))
        if not new_status:
            return Response({"detail":"Missing status"}, status=400)
        if not override and not referral.can_transition_to(new_status):
            return Response({"detail":"Invalid status transition"}, status=400)

        before = ReferralSerializer(referral).data
        referral.status = new_status
        if "owner_id" in request.data:
            referral.owner_id = request.data.get("owner_id")
        referral.save()
        after = ReferralSerializer(referral).data
        AuditLog.objects.create(actor=request.user, entity="Referral", entity_id=str(referral.id), action=f"TRANSITION_{new_status}", before=before, after=after)
        return Response(after)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserLiteSerializer(request.user).data)

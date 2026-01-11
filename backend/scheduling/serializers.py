from rest_framework import serializers
from django.contrib.auth.models import User
from core.serializers import LocationSerializer, UserLiteSerializer
from core.models import Location
from therapy.models import Program
from .models import SlotTemplate, SlotAssignment

class SlotTemplateSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(source="location", queryset=Location.objects.all(), write_only=True)
    therapist = UserLiteSerializer(read_only=True)
    therapist_id = serializers.PrimaryKeyRelatedField(source="therapist", queryset=User.objects.all(), write_only=True)

    class Meta:
        model = SlotTemplate
        fields = ["id","location","location_id","therapist","therapist_id","therapist_gender","patient_gender_allowed",
                  "day1","day2","time_start","session_minutes","room","is_active"]

class SlotAssignmentSerializer(serializers.ModelSerializer):
    slot_template = SlotTemplateSerializer(read_only=True)
    slot_template_id = serializers.PrimaryKeyRelatedField(source="slot_template", queryset=SlotTemplate.objects.all(), write_only=True)
    class Meta:
        model = SlotAssignment
        fields = ["id","slot_template","slot_template_id","program","status","held_until","created_at"]

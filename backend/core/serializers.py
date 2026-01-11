from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Location, Patient, Referral, CommunicationLog

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id","name"]

class PatientSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(source="location", queryset=Location.objects.all(), write_only=True, required=False, allow_null=True)

    class Meta:
        model = Patient
        fields = ["id","mrn","first_name","last_name","dob","gender","location","location_id",
                  "parent_name","parent_phone","parent_email","preferred_language","insurance","created_at"]

class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","first_name","last_name","email","is_staff"]

class CommunicationLogSerializer(serializers.ModelSerializer):
    created_by = UserLiteSerializer(read_only=True)
    class Meta:
        model = CommunicationLog
        fields = ["id","kind","outcome","notes","created_by","created_at"]

class ReferralSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source="patient", queryset=Patient.objects.all(), write_only=True)
    owner = UserLiteSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(source="owner", queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    communications = CommunicationLogSerializer(many=True, read_only=True)

    class Meta:
        model = Referral
        fields = ["id","patient","patient_id","referring_provider","visit_date","status",
                  "owner","owner_id","priority","due_at","notes","communications","created_at","updated_at"]

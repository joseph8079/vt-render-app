from rest_framework import serializers
from django.contrib.auth.models import User
from core.serializers import UserLiteSerializer
from .models import ClinicalReview, Program, ProgramGoal, ProgramSession, NoteTemplate, TherapyNote, GoalProgressEntry

class ClinicalReviewSerializer(serializers.ModelSerializer):
    reviewer = UserLiteSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(source="reviewer", queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    class Meta:
        model = ClinicalReview
        fields = ["id","referral","reviewer","reviewer_id","decision","summary","recommended_frequency_per_week","recommended_total_sessions","created_at","updated_at"]

class ProgramGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramGoal
        fields = ["id","title","category","baseline","target","current_progress","is_active"]

class ProgramSessionSerializer(serializers.ModelSerializer):
    therapist = UserLiteSerializer(read_only=True)
    therapist_id = serializers.PrimaryKeyRelatedField(source="therapist", queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    class Meta:
        model = ProgramSession
        fields = ["id","session_number","planned_start","planned_end","therapist","therapist_id","status","symptom_score","engagement_score","homework_compliance"]

class ProgramSerializer(serializers.ModelSerializer):
    goals = ProgramGoalSerializer(many=True, read_only=True)
    sessions = ProgramSessionSerializer(many=True, read_only=True)
    class Meta:
        model = Program
        fields = ["id","patient","referral","start_date","total_sessions","sessions_per_week","session_minutes","status","notes","goals","sessions","created_at"]

class NoteTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTemplate
        fields = ["id","name","kind","schema","is_active"]

class TherapyNoteSerializer(serializers.ModelSerializer):
    therapist = UserLiteSerializer(read_only=True)
    class Meta:
        model = TherapyNote
        fields = ["id","program","session","therapist","template","kind","data","created_at","updated_at"]

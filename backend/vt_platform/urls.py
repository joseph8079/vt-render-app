from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.api import PatientViewSet, ReferralViewSet, UserMeView
from therapy.api import ClinicalReviewViewSet, ProgramViewSet, NoteTemplateViewSet, TherapyNoteViewSet
from scheduling.api import SlotTemplateViewSet, SlotAssignmentViewSet
from dashboards.api import DashboardView

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"referrals", ReferralViewSet, basename="referral")
router.register(r"reviews", ClinicalReviewViewSet, basename="review")
router.register(r"programs", ProgramViewSet, basename="program")
router.register(r"note-templates", NoteTemplateViewSet, basename="note-template")
router.register(r"notes", TherapyNoteViewSet, basename="note")
router.register(r"slot-templates", SlotTemplateViewSet, basename="slot-template")
router.register(r"slot-assignments", SlotAssignmentViewSet, basename="slot-assignment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/me/", UserMeView.as_view(), name="me"),
    path("api/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("api/", include(router.urls)),
]

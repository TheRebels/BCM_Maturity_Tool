from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
	health, DomainViewSet, QuestionViewSet, AssessmentViewSet, ResponseViewSet, EvidenceViewSet,
	export_assessments_csv, export_assessments_pdf, export_assessments_excel,
)

router = DefaultRouter()
router.register(r'domains', DomainViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'evidence', EvidenceViewSet)

urlpatterns = [
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('health/', health, name='health'),
	path('export/csv/', export_assessments_csv, name='export_csv'),
	path('export/pdf/', export_assessments_pdf, name='export_pdf'),
	path('export/xlsx/', export_assessments_excel, name='export_excel'),
	path('', include(router.urls)),
]
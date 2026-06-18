from core.dashboard_base import StaffModelViewSet

from .filters import AdmissionFilter, ApplicationFilter, StudentFilter
from .models import Admission, Application, Student
from .serializers import AdmissionSerializer, ApplicationSerializer, StudentSerializer


class DashboardStudentViewSet(StaffModelViewSet):
    serializer_class = StudentSerializer
    filterset_class = StudentFilter
    search_fields = ['full_name', 'email', 'national_id']
    ordering_fields = ['id', 'full_name', 'email', 'status']
    ordering = ['full_name']

    def get_queryset(self):
        return Student.objects.prefetch_related('applications').all()


class DashboardAdmissionViewSet(StaffModelViewSet):
    serializer_class = AdmissionSerializer
    filterset_class = AdmissionFilter
    search_fields = ['requirements', 'procedure', 'academic_calendar']
    ordering_fields = ['id', 'tuition_fee']
    ordering = ['id']

    def get_queryset(self):
        return Admission.objects.select_related('program__department__college__university').all()


class DashboardApplicationViewSet(StaffModelViewSet):
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilter
    search_fields = ['status', 'student__full_name', 'student__email', 'program__name_ar']
    ordering_fields = ['apply_date', 'id', 'status']
    ordering = ['-apply_date']

    def get_queryset(self):
        return Application.objects.select_related(
            'student',
            'program__department__college__university',
        ).all()

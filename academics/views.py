from rest_framework import viewsets, permissions
from .models import College, Department, Program, AcademicStaff, Research
from .serializers import (
    CollegeSerializer, DepartmentSerializer, ProgramSerializer, 
    AcademicStaffSerializer, ResearchSerializer
)

class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

class AcademicStaffViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AcademicStaff.objects.all()
    serializer_class = AcademicStaffSerializer

class ResearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer

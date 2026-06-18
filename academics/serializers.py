from rest_framework import serializers
from .models import College, Department, Program, AcademicStaff, Research

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = '__all__'

class AcademicStaffSerializer(serializers.ModelSerializer):
    researches = ResearchSerializer(many=True, read_only=True)
    class Meta:
        model = AcademicStaff
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    programs = ProgramSerializer(many=True, read_only=True)
    staff = AcademicStaffSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    class Meta:
        model = College
        fields = '__all__'

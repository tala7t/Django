from rest_framework import serializers
from .models import Student, Admission, Application
from academics.serializers import ProgramSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class AdmissionSerializer(serializers.ModelSerializer):
    program_details = ProgramSerializer(source='program', read_only=True)
    class Meta:
        model = Admission
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    program_details = ProgramSerializer(source='program', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'

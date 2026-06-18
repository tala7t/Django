from rest_framework import serializers
from .models import University, Language, SocialMedia, Branch, Page, ContactMessage

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class UniversitySerializer(serializers.ModelSerializer):
    social_links = SocialMediaSerializer(many=True, read_only=True)
    branches = BranchSerializer(many=True, read_only=True)
    
    class Meta:
        model = University
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

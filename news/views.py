from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from rest_framework import viewsets, permissions

from .filters import AnnouncementFilter, EventFilter, NewsFilter
from .models import Announcement, Event, News
from .serializers import AnnouncementSerializer, EventSerializer, NewsSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.select_related('university').all().order_by('-publish_date')
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = NewsFilter
    search_fields = ['title_ar', 'title_en', 'content']
    ordering_fields = ['publish_date', 'id', 'title_ar', 'title_en']
    ordering = ['-publish_date']


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.select_related('university').all().order_by('event_date')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = EventFilter
    search_fields = ['title_ar', 'title_en', 'location', 'description']
    ordering_fields = ['event_date', 'id', 'title_ar', 'title_en']
    ordering = ['event_date']


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.select_related('university').all().order_by('-date')
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = AnnouncementFilter
    search_fields = ['title', 'body']
    ordering_fields = ['date', 'id', 'title']
    ordering = ['-date']

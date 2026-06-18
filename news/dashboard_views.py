from core.dashboard_base import StaffModelViewSet

from .filters import AnnouncementFilter, EventFilter, NewsFilter
from .models import Announcement, Event, News
from .serializers import AnnouncementSerializer, EventSerializer, NewsSerializer


class DashboardNewsViewSet(StaffModelViewSet):
    serializer_class = NewsSerializer
    filterset_class = NewsFilter
    search_fields = ['title_ar', 'title_en', 'content']
    ordering_fields = ['publish_date', 'id', 'title_ar', 'title_en']
    ordering = ['-publish_date']

    def get_queryset(self):
        return News.objects.select_related('university').all()


class DashboardEventViewSet(StaffModelViewSet):
    serializer_class = EventSerializer
    filterset_class = EventFilter
    search_fields = ['title_ar', 'title_en', 'location', 'description']
    ordering_fields = ['event_date', 'id', 'title_ar']
    ordering = ['event_date']

    def get_queryset(self):
        return Event.objects.select_related('university').all()


class DashboardAnnouncementViewSet(StaffModelViewSet):
    serializer_class = AnnouncementSerializer
    filterset_class = AnnouncementFilter
    search_fields = ['title', 'body']
    ordering_fields = ['date', 'id', 'title']
    ordering = ['-date']

    def get_queryset(self):
        return Announcement.objects.select_related('university').all()

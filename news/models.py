from django.db import models

class News(models.Model):
    university = models.ForeignKey('core.University', on_delete=models.CASCADE, related_name='news')
    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='news/')

    def __str__(self):
        return self.title_ar

class Event(models.Model):
    university = models.ForeignKey('core.University', on_delete=models.CASCADE, related_name='events')
    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')

    def __str__(self):
        return self.title_ar

class Announcement(models.Model):
    university = models.ForeignKey('core.University', on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

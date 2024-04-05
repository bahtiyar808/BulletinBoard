from django.db import models

from ckeditor.fields import RichTextField
from django.urls import reverse

from project import settings


class Announcement(models.Model):
    categories = [
        ('TA', 'Tanks'),
        ('HL', 'Hills'),
        ('DD', 'DD'),
        ('DE', 'Dealers'),
        ('GM', 'Guildmasters'),
        ('QG', 'Questgivers'),
        ('BS', 'Blacksmiths'),
        ('CU', 'Currier'),
        ('PM', 'Potion Master'),
        ('SM', 'Spell Master')
    ]
    heading = models.CharField(max_length=50)
    text = RichTextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.CharField(max_length=2, choices=categories, default='DE')
    response = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Response', related_name='announcements')
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[str(self.id)])


class Response(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    announcement = models.ForeignKey(
        to=Announcement,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)


class News(models.Model):
    heading = models.CharField(max_length=50)
    text = RichTextField()

# Create your models here.

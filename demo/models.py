from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('demo.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Provider(models.Model):
    provider_id = models.CharField(max_length=12)
    tax_id = models.CharField(max_length=12)
    npi = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    practice_name = models.CharField(max_length=50)
    term_date = models.DateTimeField(
        blank=False, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('auth.User')
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=2, null=True)
    zip = models.CharField(max_length=10, null=True)
    office_phone = models.CharField(max_length=20, null=True)
    mobile_phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=40, null=True)
    social = models.CharField(max_length=40, null=True)
    specialty = models.CharField(max_length=40, null=True)
    languages = models.CharField(max_length=20, null=True)
    next_appt = models.DateTimeField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.provider_id

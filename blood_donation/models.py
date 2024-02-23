from account.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify, Truncator
from markdown import markdown
from .utils import unique_slug_generator


# Create your models here.


class BloodDonor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.CharField('Blood Group', choices=(('A+', 'A+'),
                                                     ('A-', 'A-'),
                                                     ('B+', 'B+'),
                                                     ('B-', 'B-'),
                                                     ('O+', 'O+'),
                                                     ('O-', 'O-'),
                                                     ('AB+', 'AB+'),
                                                     ('AB-', 'AB-')),
                             max_length=3)
    last_donate = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username + " " + self.group)
        super(BloodDonor, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-update_at']


class DonationPostQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                        Q(title__icontains=query) |
                        Q(group__icontains=query) |
                        Q(place__icontains=query) |
                        Q(about__icontains=query)
            )
            qs = qs.filter(or_lookup).all()
        return qs


class DonationPostManager(models.Manager):
    def get_queryset(self):
        return DonationPostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class DonationPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    by = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    group = models.CharField('Blood Group Need', choices=(('A+', 'A+'),
                                                          ('A-', 'A-'),
                                                          ('B+', 'B+'),
                                                          ('B-', 'B-'),
                                                          ('O+', 'O+'),
                                                          ('O-', 'O-'),
                                                          ('AB+', 'AB+'),
                                                          ('AB-', 'AB-')),
                             max_length=3, null=True, blank=True)
    place = models.CharField(max_length=100)
    about = models.TextField('Patient Details', null=True, blank=True)
    contact_number = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = DonationPostManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-update_at']


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=DonationPost)


class Comment(models.Model):
    message = models.TextField(max_length=4000)
    donation = models.ForeignKey(DonationPost, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coments')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_comments_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

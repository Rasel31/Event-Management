from account.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify, Truncator
from markdown import markdown

# Create your models here.


class EventQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                        Q(offer_by__icontains=query) |
                        Q(category__icontains=query) |
                        Q(designation__icontains=query) |
                        Q(name__icontains=query) |
                        Q(venue__icontains=query) |
                        Q(chief__icontains=query) |
                        Q(objective__icontains=query) |
                        Q(outcome__icontains=query)
            )
            qs = qs.filter(or_lookup).all()
        return qs


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Event(models.Model):

    category = models.CharField(max_length=10, choices=(
        ('Recent', 'Recent'),
        ('OnGoing', 'OnGoing'),
        ('UpComing', 'UpComing')
    ), null=True, blank=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_by = models.CharField('Program Offered by', max_length=250, help_text='Department/Section/Club/others name')
    by = models.CharField('Person Responsible', max_length=100)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True, width_field='width', height_field='height')
    designation = models.CharField(max_length=100)
    mobile = models.CharField(max_length=14)
    name = models.CharField('Program Name', max_length=500)
    venue = models.CharField(max_length=100)
    chief = models.CharField('Chief Guest', max_length=100)
    objective = models.TextField('Objectives of the Program')
    start = models.DateTimeField('Start Time', auto_now_add=False)
    end = models.DateTimeField('End Time', auto_now_add=False)
    target = models.CharField('Target Audience', max_length=100)
    number = models.PositiveIntegerField('Expected Number', default=50)
    outcome = models.TextField('Object Outcome of the Event', null=True, blank=True,
                               help_text='Mention How the Intended Benefit of the Program will be Achieved')
    approval = models.CharField("Program Approval", max_length=100, null=True, blank=True,
                                help_text='Responsible person\'s name with mobile number')
    booking = models.CharField("Venue Booking", max_length=100, null=True, blank=True,
                               help_text='Responsible person\'s name with mobile number')
    reception = models.CharField("Guest Reception", max_length=100, null=True, blank=True,
                                 help_text='Responsible person\'s name with mobile number')

    parking = models.CharField("Car Parking", max_length=100, null=True, blank=True,
                               help_text='Responsible person(s) name with mobile number')
    it = models.CharField('IT Support', max_length=100, null=True, blank=True,
                          help_text='Responsible person\'s name with mobile number')
    banner = models.CharField("Banner Text & Size", max_length=100, null=True, blank=True,
                              help_text='Responsible person\'s name with mobile number')
    security = models.CharField(max_length=100, null=True, blank=True,
                                help_text='Responsible person\'s name with mobile number')
    public_relation = models.CharField("Public Relation", max_length=100, null=True, blank=True,
                                       help_text='Responsible person\'s name with mobile number')
    press = models.CharField("Press Release & Website Text", max_length=100, null=True, blank=True,
                             help_text='Responsible person\'s name with mobile number')
    recording = models.CharField("Video Recording", max_length=100, null=True, blank=True,
                                 help_text='Responsible person\'s name with mobile number')
    tv = models.CharField('Campus TV', max_length=100, null=True, blank=True,
                          help_text='Responsible person\'s name with mobile number')
    decoration = models.CharField("Venue Decoration", max_length=100, null=True, blank=True,
                                  help_text='Responsible person\'s name with mobile number')
    supervision = models.CharField("Cleaning Supervision", max_length=100, null=True, blank=True,
                                   help_text='Responsible person\'s name with mobile number')
    Refreshment = models.CharField(max_length=100, null=True, blank=True,
                                   help_text='Responsible person\'s name with mobile number')
    support = models.CharField("Staff Support", max_length=100, null=True, blank=True,
                               help_text='Responsible person\'s name with mobile number')
    transport = models.CharField("Transport Booking", max_length=100, null=True, blank=True,
                                 help_text='Responsible person\'s name with mobile number')
    extsupport = models.CharField("Extra Support from Outside", max_length=100, null=True, blank=True,
                                  help_text='Responsible person\'s name with mobile number')
    others = models.CharField("Others Requirement", max_length=100, null=True, blank=True,
                              help_text='Responsible person\'s name with mobile number')
    master = models.CharField("Master of Ceremonies", max_length=100, null=True, blank=True,
                              help_text='Responsible person\'s name with mobile number')
    outline = models.CharField("Program Outline & Sequence Confirmed", max_length=100, null=True, blank=True,
                               help_text='Responsible person\'s name with mobile number')
    training = models.CharField("Volunteers & Training", max_length=100, null=True, blank=True,
                                help_text='Responsible person\'s name with mobile number')
    budget = models.CharField("Budget Source", max_length=100, null=True, blank=True,
                              help_text='Responsible person\'s name with mobile number')
    contribution = models.CharField("Departmental Contribution", max_length=100, null=True, blank=True,
                                    help_text='Responsible person\'s name with mobile number')
    sponsor = models.CharField("Sponsor Contribution", max_length=100, null=True, blank=True,
                               help_text='Responsible person\'s name with mobile number')
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EventManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('swehome:event-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-update']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)


class Comment(models.Model):

    message = models.TextField(max_length=4000)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_comments_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    class Meta:
        ordering = ['-created_at']

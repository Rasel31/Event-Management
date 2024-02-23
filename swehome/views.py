from itertools import chain

from blood_donation.models import DonationPost
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from easy_pdf.views import PDFTemplateResponseMixin
from swehome.forms import CommentForm, EventCreateForm
from .models import Event
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


def home_view(request):

    recent = Event.objects.filter(category='Recent', approved=True)[:3]
    ongoing = Event.objects.filter(category='OnGoing', approved=True)[:3]
    upcoming = Event.objects.filter(category='UpComing', approved=True)[:3]

    context = {
        'recent': recent,
        'ongoing': ongoing,
        'upcoming': upcoming
    }

    return render(request, 'home.html', context)


@login_required
def event_create_view(request):

    template_name = 'swehome/event-create.html'

    if request.method == 'POST':
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.approved = False
            instance.user = request.user
            instance.save()
            messages.add_message(request, messages.SUCCESS, 'Event Created Successfully! Wait For Approve. Thank You.')
            return redirect('swehome:event-list')
    else:
        form = EventCreateForm()
    return render(request, template_name, {'form': form})


class EventDetail(DetailView):

    queryset = Event.objects.all()


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'swehome/event_update.html'
    context_object_name = 'object'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.update = timezone.now()
        post.save()
        messages.add_message(self.request, messages.SUCCESS, 'Event Updated Successfully!')
        return redirect('swehome:event-detail', slug=post.slug)


class EventList(ListView):

    def get_queryset(self):
        queryset = Event.objects.filter(
            Q(approved=True) &
            Q(category__icontains='upcoming') |
            Q(category__icontains='ongoing')
        ).order_by('category')
        return queryset


class MyEventList(LoginRequiredMixin, ListView):

    template_name = 'swehome/my_event_list.html'

    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user)
        return queryset


class ArchivedEventList(LoginRequiredMixin, ListView):

    template_name = 'swehome/archived_event_list.html'

    def get_queryset(self):
        queryset = Event.objects.filter(approved=True, category__icontains='recent')
        return queryset


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('swehome:my-event-list')


class EventPDFView(LoginRequiredMixin, PDFTemplateResponseMixin, DetailView):

    template_name = 'swehome/event-form.html'

    def get_object(self, *args, **kwargs):

        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Event, slug=slug)
        return obj

# class EventForm(DetailView):
#
#     template_name = 'swehome/event-form.html'
#
#     def get_object(self, *args, **kwargs):
#
#         slug = self.kwargs.get('slug')
#         obj = get_object_or_404(Event, slug=slug)
#         return obj


@login_required
def reply_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.event = event
            post.created_by = request.user
            post.save()

            post.last_updated = timezone.now()
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Thanks for your reply.')
            event_url = reverse('swehome:event-detail', kwargs={'slug': event.slug})
            return redirect(event_url)
    else:
        form = CommentForm()
    return render(request, 'swehome/reply_event.html', {'event': event, 'form': form})


class SearchView(ListView):
    template_name = 'search.html'
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            event_results = Event.objects.search(query)
            donationpost_results = DonationPost.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                    event_results,
                    donationpost_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)    # since qs is actually a list
            return qs

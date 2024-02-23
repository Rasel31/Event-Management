from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, TemplateView
from swehome.models import Event
from .models import User
from .forms import ModeratorSignUpForm, SecretarySignUpForm, StudentSignUpForm, EventApproveForm
from django.contrib import messages
from .decorators import head_required, head_moderator_required
from django.contrib.auth.decorators import login_required
# Create your views here.


@method_decorator(login_required, name='dispatch')
@method_decorator(head_required, name='dispatch')
class SignUpView(TemplateView):
    template_name = 'account/head/registration/signup.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(head_required, name='dispatch')
class ModeratorSignUpView(CreateView):
    model = User
    form_class = ModeratorSignUpForm
    template_name = 'account/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Moderator '
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Sign Up Successfully!')
        return redirect('/')


@method_decorator(login_required, name='dispatch')
@method_decorator(head_moderator_required, name='dispatch')
class SecretarySignUpView(CreateView):
    model = User
    form_class = SecretarySignUpForm
    template_name = 'account/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Secretary '
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Sign Up Successfully!')
        return redirect('/')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Student '
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'Registration Completed Successfully! Please Contact to SWE Office For Site Access.')
        return redirect('/')


@login_required
@head_moderator_required
def event_approval_list(request):

    q = Event.objects.filter(approved=False)

    context = {
        'approve': q,
    }
    return render(request, 'account/event-approve-list.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(head_moderator_required, name='dispatch')
class EventApproveView(UpdateView):

    form_class = EventApproveForm
    template_name = 'account/event-approve.html'

    def get_object(self, *args, **kwargs):

        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Event, slug=slug)
        return obj


from blood_donation.forms import CommentForm, BloodDonationForm, BloodInfoForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from .models import BloodDonor, DonationPost
from django.contrib.auth.decorators import login_required
# Create your views here.


def blood_donate_view(request):

    query = DonationPost.objects.all()[:10]

    context = {
        'posts': query,
    }
    return render(request, 'blood_donation/blood-home.html', context)


@login_required
def add_blood_info(request):
    if request.method == 'POST':
        form = BloodInfoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            a = BloodDonor.objects.filter(user=request.user).exists()
            if a:
                messages.add_message(request, messages.WARNING, 'You Already Added Information')
                return redirect('blood_donation:blood-home')
            post.user = request.user
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Information Added Successfully!')
            return redirect('blood_donation:blood-info')
    else:
        form = BloodInfoForm()
    return render(request, 'blood_donation/blood-info.html', {'form': form})


@login_required
def my_blood_info(request):
    me = BloodDonor.objects.filter(user=request.user)

    context = {
        'object': me
    }
    return render(request, 'blood_donation/blooddonor_detail.html', context)


class BloodInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = BloodDonor
    form_class = BloodInfoForm
    template_name = 'blood_donation/blood-info-update.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Information Updated Successfully!')
        return redirect('blood_donation:blood-info')


@login_required
def blood_donation_post(request):

    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('blood_donation:blood-home')
    else:
        form = BloodDonationForm()
    return render(request, 'blood_donation/add-post.html', {'form': form})


@login_required
def my_donation_post_list(request):

    q = DonationPost.objects.filter(owner=request.user)

    context = {
        'list': q,
    }
    return render(request, 'blood_donation/donationpost_list.html', context)


class PostDetailView(DetailView):
    queryset = DonationPost.objects.all()


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = DonationPost
    form_class = BloodDonationForm
    template_name = 'blood_donation/post-update.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def form_valid(self, form):
        instance=form.save(commit=False)
        instance.save()
        messages.add_message(self.request, messages.SUCCESS, 'Post Updated Successfully!')
        return redirect('blood_donation:post-detail', slug=instance.slug)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = DonationPost
    success_url = reverse_lazy('blood_donation:blood-home')


@login_required
def reply_donation(request, slug):
    donation = get_object_or_404(DonationPost, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.donation = donation
            post.created_by = request.user
            post.save()

            post.last_updated = timezone.now()
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Thanks for your reply.')
            donation_url = reverse('blood_donation:post-detail', kwargs={'slug': donation.slug})
            return redirect(donation_url)
    else:
        form = CommentForm()
    return render(request, 'blood_donation/reply_donation.html', {'donation': donation, 'form': form})

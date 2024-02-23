from account.models import User, Student, Moderator, Secretary
from swehome.models import Event
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms


class ModeratorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_moderator = True
        if commit:
            user.save()

        Moderator.objects.create(user=user)
        return user


class SecretarySignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_secretary = True
        user.save()
        Secretary.objects.create(user=user)
        return user


class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.is_active = False
        user.save()
        Student.objects.create(user=user)
        return user


class EventApproveForm(forms.ModelForm):

    approved = forms.BooleanField(widget=forms.CheckboxInput, required=True)

    class Meta:
        model = Event

        fields = [
            'approved'
        ]

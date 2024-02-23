from django import forms
from .models import Comment, BloodDonor, DonationPost


class BloodInfoForm(forms.ModelForm):
    class Meta:
        model = BloodDonor
        fields = [
            'group', 'last_donate'
        ]


class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = DonationPost
        fields = [
            'by', 'title', 'group', 'place', 'about', 'contact_number'
        ]


class CommentForm(forms.ModelForm):

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'What is in your mind?'}
        ), max_length=4000, help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Comment
        fields = [
            'message',
        ]
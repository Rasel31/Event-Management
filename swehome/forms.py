from django import forms
from swehome.models import Comment, Event


class EventCreateForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            'offer_by', 'by', 'image', 'designation', 'mobile', 'name', 'venue', 'chief', 'objective', 'start', 'end',
            'target', 'number', 'outcome', 'approval', 'booking', 'reception', 'parking', 'it', 'banner', 'security',
            'public_relation', 'press', 'recording', 'tv', 'decoration', 'supervision', 'Refreshment', 'support',
            'transport', 'extsupport', 'others', 'master', 'outline', 'training', 'budget', 'contribution', 'sponsor'
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


from django import forms

# from .models import Post, Comment, UserProfile
from .models import Post, Comment
from .models import Provider, Message, CountyData

import logging
logger = logging.getLogger(__name__)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # exclude = ['author', 'updated', 'created', ]
        fields = ['title', 'text']
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'Say something...'}
            ),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = ('name', 'description',)


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = (
            'message_from', 'message_to',
            'text', 'member', )


class SmsForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'required': True, 'rows': '2',
                    'placeholder': 'Text to member...',
                    'class': 'form-control'}
            ),
        }


class CountyDataForm(forms.ModelForm):
    # state = forms.ChoiceField(choices=[
    #     ('NY', 'New York'), ('NJ', 'New Jersey')], required=False)
    state = forms.ChoiceField(choices=[], required=True)
    county = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = CountyData
        fields = ('state', 'county',)

    def __init__(self, *args, **kwargs):
        super(CountyDataForm, self).__init__(*args, **kwargs)
        states = CountyData.objects.all().values_list(
            "state", "state_name").distinct().order_by('state_name')
        BLANK_CHOICE = (('', '---------'),)
        state_choices = BLANK_CHOICE + tuple(states)
        self.fields['state'].choices = state_choices


# SC: Add picture
# http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example
# class UserProfileForm(forms.Form):
#     phone = forms.CharField(max_length=20)
#     picture = forms.ImageField(
#         label='Select a file',
#         help_text='max. 42 megabytes'
#     )
# class UserProfileForm(forms.ModelForm):

#     class Meta:
#         model = UserProfile
#         fields = ('phone', 'picture',)

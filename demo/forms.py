from django import forms

# from .models import Post, Comment, UserProfile
from .models import Post, Comment, Provider, Message


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


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

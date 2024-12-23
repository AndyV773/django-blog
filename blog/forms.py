from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for submitting a comment to a single post.
    """
    class Meta:
        model = Comment
        fields = ('body',)

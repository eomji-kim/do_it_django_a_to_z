from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # exclude = ('post', 'author', 'created_at', 'modified_at', ) 로도 사용 가능
        fields = ('content',)
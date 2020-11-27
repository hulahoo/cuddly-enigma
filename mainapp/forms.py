from django import forms

from mainapp.models import Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('product', 'comment', 'rate')

class EditPost(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'rate')


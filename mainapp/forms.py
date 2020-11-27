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


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
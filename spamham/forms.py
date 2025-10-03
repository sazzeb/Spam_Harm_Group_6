from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(
        label="Message",
        max_length=10000,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Type a message..."}),
    )

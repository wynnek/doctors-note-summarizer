from django import forms

class SummarizerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "medical-note-textarea",
                "class": "form-control",
                "style": "height: 200px;",
                "placeholder": "Enter the medical note here:"
            }), label="")
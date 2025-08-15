from django import forms
from .models import ContactSubmission, NewsletterSubscription, JobOpening, JobApplication

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4, 'required': True}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'required': True, 'placeholder': 'Enter your email'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Search...',
    }))

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'position', 'resume', 'cover_letter']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'position': forms.Select(attrs={'class': 'w-full p-2 border rounded', 'required': True}),
            'resume': forms.FileInput(attrs={'class': 'w-full p-2 border rounded', 'required': True, 'accept': '.pdf'}),
            'cover_letter': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4, 'required': True}),
        }
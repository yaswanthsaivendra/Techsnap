from .models import Blogs
from django import forms

class BlogsForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'name': 'body'})
        }

    def __init__(self, *args, **kwargs):
        super(BlogsForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ""
from django.forms import ModelForm
from .models import Project
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','image','demo_link','source_link','tags','vote_total','vote_ratio']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for label, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})
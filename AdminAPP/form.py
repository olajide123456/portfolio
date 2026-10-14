from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
     class Meta:
        model = Project

        fields = ['title','category','description','image','technologies','project_url','github_url','status','display_order', ]
     widgets = {
        'title': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Example: E-Commerce Website',
            }
        ),
        'category': forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        'description': forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write a brief description about this project...',
                'rows': 5,
            }
        ),
        'image': forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }
        ),
        'technologies': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Python, Django, HTML, CSS, Bootstrap',
            }
        ),
        'project_url': forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }
        ),
        'github_url': forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/project',
            }
        ),
        'status': forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        'display_order': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Example: 1',
                'min': '1',
            }
        ),

    }

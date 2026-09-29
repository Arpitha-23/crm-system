
from django import forms

from .models import Lead, Activity



class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'company',
            'job_title',
            'status',
            'source',
            'notes',
            'assigned_to',
        ]

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'company': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'job_title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'source': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'assigned_to': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity

        fields = [
            'activity_type',
            'subject',
            'description',
            'due_date',
            'completed',
        ]

        widgets = {

            'activity_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Follow-up call'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Add details about this activity...'
                }
            ),

            'due_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),

            'completed': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }


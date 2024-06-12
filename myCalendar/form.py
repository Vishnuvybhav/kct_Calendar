from django.forms import ModelForm, DateInput
from .models import Event, Category,Colabrations,AccessLevels
from django import forms

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_date", "end_date", "college", "location", "category"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_date": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_date": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "college": forms.Select(attrs={"class": "form-control"}),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event location"}
            ),
            "category": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

        def __init__(self, *args, **kwargs):
            super(EventForm, self).__init__(*args, **kwargs)
            # input_formats to parse HTML5 datetime-local input to datetime field
            self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
            self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


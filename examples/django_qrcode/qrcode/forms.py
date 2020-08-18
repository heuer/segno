from django import forms
from django.core.validators import RegexValidator


class TicketForm(forms.Form):
    """Simple form for the Ticket model."""
    name = forms.CharField(label='Name', max_length=150, min_length=1,
                           validators=[RegexValidator(r'^[A-Z0-9]+$')])

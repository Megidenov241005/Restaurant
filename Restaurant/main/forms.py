from django import forms
from django.utils import timezone
from .models import Reserve

class ReserveTimeForm(forms.Form):
    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and start < timezone.now():
            self.add_error('start', 'Нельзя бронировать на прошлое время.')

        if start and end and end <= start:
            self.add_error('end', 'Время окончания должно быть позже начала.')
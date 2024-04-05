from django import forms
from .models import Tournament

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'sport']
        labels = {
            'name': 'Nom du tournoi',
            'sport': 'Choisir le sport du tournoi',
        }

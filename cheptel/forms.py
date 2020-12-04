from django import forms

from .models import Animal, Equipement

class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = ('id_animal', 'race', 'type', 'photo')


from django import forms
from .models import Module, Flashcard

class ModuleEditingForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'title-input', 
                'id': 'title-id'
                }),
            'description': forms.TextInput(attrs={
                'class': 'description-input', 
                'placeholder': 'Добавьте описание...'}),
        }

class CardEditingForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = '__all__'

        widgets = {
            'word_front': forms.TextInput(attrs={
                'class': 'card-term-input', 
                }),
            'word_back': forms.TextInput(attrs={
                'class': 'card-definition-input', 
                }),    
        }

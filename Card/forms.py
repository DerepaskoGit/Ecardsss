from django import forms
from .models import Module
from django.db import connection

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

def get_dynamic_form_class(table_name):
    class DynamicForm(forms.Form):
        type_card = forms.ChoiceField(choices=[('simple', 'Simple'), ('phrase', 'Phrase'), ('test', 'Test')])
        word_front = forms.CharField(max_length=20, required=False)
        word_back = forms.CharField(max_length=20, required=False)
        phrase_front = forms.CharField(max_length=200, required=False)
        phrase_back = forms.CharField(max_length=200, required=False)
        image = forms.FileField(required=False)
        audio_word_front = forms.FileField(required=False)
        audio_word_back = forms.FileField(required=False)
        audio_phrase_front = forms.FileField(required=False)
        audio_phrase_back = forms.FileField(required=False)

        def __init__(self, *args, **kwargs):
            self.table_name = kwargs.pop('table_name', None)  # Забираем table_name
            super().__init__(*args, **kwargs)

        def save(self):
            """Сохранение данных в нужную таблицу"""
            if not self.table_name:
                raise ValueError("Table name is not set for this form!")

            cleaned_data = self.cleaned_data
            if cleaned_data:  # Если форма заполнена
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                            INSERT INTO {self.table_name} 
                            (type_card, word_front, word_back, phrase_front, phrase_back, image, 
                             audio_word_front, audio_word_back, audio_phrase_front, audio_phrase_back)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        [
                            cleaned_data['type_card'], cleaned_data['word_front'], cleaned_data['word_back'], 
                            cleaned_data['phrase_front'], cleaned_data['phrase_back'], cleaned_data['image'], 
                            cleaned_data['audio_word_front'], cleaned_data['audio_word_back'], 
                            cleaned_data['audio_phrase_front'], cleaned_data['audio_phrase_back']
                        ]
                    )

    return DynamicForm



# def get_dynamic_form(tabel_name, data=None):

#     fields = {
#         'type_card':forms.ChoiceField(choices=['simple', 'phrase', 'test']),
#         'word_front':forms.CharField(max_length=20, required=False),
#         'word_back':forms.CharField(max_length=20, required=False),
#         'phrase_front':forms.CharField(max_length=200, required=False),
#         'phrase_back':forms.CharField(max_length=200, required=False),
#         'image':forms.FileField(required=False),
#         'audio_word_front':forms.FileField(required=False),
#         'audio_word_back':forms.FileField(required=False),
#         'audio_phrase_front':forms.FileField(required=False),
#         'audio_phrase_back':forms.FileField(required=False),
#     }

#     DynamicForm = type('DynamicForm', (forms.Form, ), fields)
#     return DynamicForm(data) if data else DynamicForm()
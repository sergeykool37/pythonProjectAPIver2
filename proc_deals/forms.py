from django import forms

class FileFrom(forms.Form):
    file = forms.FileField(label = 'Имя файла',)
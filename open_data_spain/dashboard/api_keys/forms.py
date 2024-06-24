from django import forms

from authentication.models import APIKey


class CreateAPIKey(forms.ModelForm):
    class Meta:
        model = APIKey
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la API'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.key = APIKey.generate_random_api_keys()

        if commit:
            instance.save()

        return instance

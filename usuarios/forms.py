from django import forms
from django.contrib.auth.models import User


class RegistrarForm(forms.Form):
    nome = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    profissao = forms.CharField(required=True)

    def is_valid_from_form(self):
        return super(RegistrarForm, self).is_valid()

    def is_valid(self):
        valid = self.is_valid_from_form()
        if not super(RegistrarForm, self).is_valid():
            print(self.cleaned_data)
            self.add_error(field=forms.ALL_FIELDS, error='Por favor, verifique os dados informados')
            valid = False
            user_exists = User.objects.filter(username=self.cleaned_data['nome']).exists()
            if user_exists:
                self.add_error(field=forms.ALL_FIELDS, error='Usuário já existente.')
                valid = False
        return valid
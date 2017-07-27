from django import forms

from agenda.models import Cliente


class EditarPerfilForm(forms.Form):

    nome = forms.CharField(required=True)
    profissao = forms.CharField(required=True)
    telefone = forms.CharField(required=True)

    def is_valid_from_form(self):
        return super(EditarPerfilForm, self).is_valid()

    def is_valid(self):
        valid = self.is_valid_from_form()
        if not super(EditarPerfilForm, self).is_valid():
            self.add_error(field=forms.ALL_FIELDS, error='Por favor, verifique os dados informados')
            valid = False
        return valid

class RemarcarForm(forms.Form):

    data = forms.DateField(required=True)
    horario = forms.TimeField(required=True)

    def is_valid_from_form(self):
        return super(RemarcarForm, self).is_valid()

    def is_valid(self):
        valid = self.is_valid_from_form()
        if not super(RemarcarForm, self).is_valid():
            self.add_error(field=forms.ALL_FIELDS, error='Por favor, verifique os dados informados')
            valid = False
        return valid

class MarcarForm(forms.Form):

    data = forms.DateField(required=True)
    horario = forms.TimeField(required=True)
    nome = forms.CharField(required=True, max_length=30)
    profissional = forms.CharField(required=True)
    cpf = forms.CharField(required=True)
    telefone = forms.CharField(required=True)

    def is_valid_from_form(self):
        return super(MarcarForm, self).is_valid()

    def is_valid(self):
        valid = self.is_valid_from_form()
        print(self.cleaned_data)
        if not super(MarcarForm, self).is_valid():
            self.add_error(field=forms.ALL_FIELDS, error='Por favor, verifique os dados informados')
            valid = False
        return valid

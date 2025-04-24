from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'email', 'phone', 'group']

        labels = {
            'name': _('Nome'),
            'email': _('E-mail'),
            'phone': _('Telefone'),
            'group': _('Grupo'),
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'data-mask': '(00) 00000-0000',
            }),
            'group': forms.RadioSelect(),
        }

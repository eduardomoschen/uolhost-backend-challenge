from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from . import forms, models
import requests
import xml.etree.ElementTree as ET


class PlayerListView(ListView):
    model = models.Player
    template_name = 'players_list.html'
    context_object_name = 'players'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(alias__icontains=q) |
                Q(group__icontains=q)
            )

        return queryset


class PlayerCreateView(CreateView):
    model = models.Player
    form_class = forms.PlayerForm
    template_name = 'player_create.html'
    success_url = reverse_lazy('player_list')


    def form_valid(self, form):
        group = form.cleaned_data['group']
        alias, reference = self.search_available_alias(group)

        if alias:
            player = form.save(commit=False)
            player.alias = alias
            player.reference = reference
            player.save()

            messages.success(self.request, 'Jogador castrado com sucesso.')
            return super().form_valid(form)
        else:
            form.add_error('group', 'A lista selecionada não tem codinomes disponíveis.')
            messages.error(self.request, 'Falha ao cadastrar o jogador.')
            return self.form_invalid(form)


    def search_available_alias(self, group):
        useds = models.Player.objects.values_list('alias', flat=True)

        if group == models.Group.AVENGERS:
            url = 'https://raw.githubusercontent.com/uolhost/test-backEnd-Java/master/referencias/vingadores.json'

            try:
                response = requests.get(url)
                heroes = response.json()
                for hero in heroes['vingadores']:
                    name = hero['codinome'].strip()
                    if name not in useds:
                        return name, 'vingadores.json'
            except Exception:
                return None, None
        elif group == models.Group.JUSTICE_LEAGUE:
            url = 'https://raw.githubusercontent.com/uolhost/test-backEnd-Java/master/referencias/liga_da_justica.xml'

            try:
                response = requests.get(url)
                root = ET.fromstring(response.content)

                for alias in root.findall('.//codinome'):
                    name = alias.text.strip()

                    if name not in useds:
                        return name, 'liga_da_justica.xml'
            except Exception:
                return None, None

        return None, None




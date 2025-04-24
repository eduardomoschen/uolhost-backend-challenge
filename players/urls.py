from django.urls import path
from players import views


urlpatterns = [
    path('players/list/', views.PlayerListView.as_view(), name='player_list'),
    path('players/create/', views.PlayerCreateView.as_view(), name='player_create'),
]

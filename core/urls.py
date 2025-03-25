from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.CadastroView.as_view(), name='cadastro'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('avaliar/', views.avaliar_bairro, name='avaliar_bairro'),
    path('minhas-avaliacoes/', views.minhas_avaliacoes, name='minhas_avaliacoes'),
]

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bairro, Avaliacao
from .forms.auth_forms import CadastroForm
from .forms.bairro_forms import AvaliacaoForm


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


class CadastroView(CreateView):
    template_name = 'core/cadastro.html'
    form_class = CadastroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(*args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Formulário para avaliação
        context['form'] = AvaliacaoForm()

        # Obter dados para o gráfico
        bairros = Bairro.objects.all()
        dados_grafico = []

        for bairro in bairros:
            media = bairro.avaliacoes.aggregate(
                media=Avg('nota'))['media'] or 0
            dados_grafico.append({
                'nome': bairro.nome,
                'media': round(media, 1)
            })

        # Ordenar do melhor para o pior
        dados_grafico = sorted(
            dados_grafico, key=lambda x: x['media'], reverse=True)

        context['dados_grafico'] = dados_grafico

        # Últimas avaliações
        context['avaliacoes_recentes'] = Avaliacao.objects.all().order_by(
            '-data_criacao')[:10]

        return context


@login_required
def avaliar_bairro(request):
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user

            # Converter a nota de string para inteiro
            avaliacao.nota = int(form.cleaned_data['nota'])

            # Obter ou criar o bairro pelo nome
            nome_bairro = form.cleaned_data['bairro']
            bairro, _ = Bairro.objects.get_or_create(nome=nome_bairro)
            avaliacao.bairro = bairro

            # Verificar se já existe avaliação para este bairro por este usuário
            avaliacao_existente = Avaliacao.objects.filter(
                usuario=request.user,
                bairro=bairro
            ).first()

            if avaliacao_existente:
                # Atualizar avaliação existente
                avaliacao_existente.nota = int(form.cleaned_data['nota'])
                avaliacao_existente.comentario = form.cleaned_data['comentario']
                avaliacao_existente.save()
                messages.success(
                    request, 'Sua avaliação foi atualizada com sucesso!')
            else:
                # Criar nova avaliação
                avaliacao.save()
                messages.success(
                    request, 'Sua avaliação foi registrada com sucesso!')

            return redirect('home')
    else:
        form = AvaliacaoForm()

    return render(request, 'core/home.html', {'form': form})


@login_required
def minhas_avaliacoes(request):
    avaliacoes = Avaliacao.objects.filter(
        usuario=request.user).order_by('-data_criacao')
    return render(request, 'core/minhas_avaliacoes.html', {'avaliacoes': avaliacoes})

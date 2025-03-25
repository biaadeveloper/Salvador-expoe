from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Bairro(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
        ordering = ['nome']


class Avaliacao(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='avaliacoes')
    bairro = models.ForeignKey(
        Bairro, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    comentario = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario.username} para {self.bairro.nome}: {self.nota}"

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-data_criacao']
        # Garantir que um usuário só possa avaliar um bairro uma vez
        unique_together = ('usuario', 'bairro')


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil')
    data_nascimento = models.DateField()
    aceita_localizacao = models.BooleanField(default=False)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

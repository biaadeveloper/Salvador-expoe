from core.models import Bairro
import os
import django

# Configurar as variáveis de ambiente para o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')
django.setup()


# Lista de bairros de Salvador
bairros = [
    'Barra',
    'Itapuã',
    'Pituba',
    'Rio Vermelho',
    'Amaralina',
    'Bonfim',
    'Cajazeiras',
    'Cabula',
    'Piatã',
    'Itaigara',
    'Ondina',
    'Pelourinho',
    'Liberdade',
    'Brotas',
    'Graça',
    'Canela',
    'Federação',
    'Boca do Rio',
    'Costa Azul',
    'Stella Maris',
    'Barris',
    'Campo Grande',
    'Comércio',
    'Nazaré',
    'São Caetano',
    'Paripe',
    'Periperi',
    'Mussurunga',
    'Tancredo Neves',
    'Pau da Lima'
]

# Adicionar bairros ao banco de dados
for nome_bairro in bairros:
    Bairro.objects.get_or_create(nome=nome_bairro)
    print(f'Bairro "{nome_bairro}" adicionado.')

print(f"Total de bairros: {Bairro.objects.count()}")

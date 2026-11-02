
from src.data_loader import carregar_dados, carregar_politicas

# Carrega os dados
dados = carregar_dados()

print("DADOS CARREGADOS:\n")

for nome, tabela in dados.items():
    print(f"{nome}: {len(tabela)} registros")

# Carrega as políticas
politicas = carregar_politicas()

print("\nPOLÍTICAS CARREGADAS:")
print(f"{len(politicas)} caracteres de texto")

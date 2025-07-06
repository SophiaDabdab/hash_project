import csv

# Funções de hashing (exemplo com módulo/divisão)
def hash_divisao(chave, tamanho):
    return hash(chave) % tamanho

def hash_multiplicacao(chave, tamanho):
    A = 0.6180339887  # constante (parte fracionária do número de ouro)
    return int(tamanho * ((hash(chave) * A) % 1))

class HashTable:
    def __init__(self, tamanho=100, funcao_hash=hash_divisao):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(tamanho)]  # Encadeamento exterior
        self.funcao_hash = funcao_hash

    def _endereco(self, chave):
        return self.funcao_hash(chave, self.tamanho)

    def inserir(self, chave, valor):
        indice = self._endereco(chave)
        for par in self.tabela[indice]:
            if par[0] == chave:
                return  # Duplicata detectada, ignora
        self.tabela[indice].append((chave, valor))

    def buscar(self, chave):
        indice = self._endereco(chave)
        for par in self.tabela[indice]:
            if par[0] == chave:
                return par[1]
        return None

    def remover(self, chave):
        indice = self._endereco(chave)
        for i, par in enumerate(self.tabela[indice]):
            if par[0] == chave:
                del self.tabela[indice][i]
                return True
        return False

    def valores(self):
        for bucket in self.tabela:
            for _, valor in bucket:
                yield valor

# -------------------------------
# Função de deduplicação em CSV
# -------------------------------

def remover_duplicatas_csv(caminho_csv, chave_coluna, separador=','):
    hash_table = HashTable(tamanho=1000, funcao_hash=hash_divisao)

    with open(caminho_csv, newline='', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=separador)
        for linha in leitor:
            chave = linha[chave_coluna]
            hash_table.inserir(chave, linha)

    return list(hash_table.valores())

# with open("exemplo.csv", newline='', encoding='utf-8') as arquivo:
#     leitor = csv.DictReader(arquivo)
#     for linha in leitor:
#         print(linha)

# -------------------------------
# Exemplo de uso:
# -------------------------------

if __name__ == "__main__":
    caminho = "exemplo.csv"
    chave = "cpf"  # ou "id", "email", dependendo do seu CSV

    dados_sem_duplicatas = remover_duplicatas_csv(caminho, chave)

    print("Registros únicos:")
    for registro in dados_sem_duplicatas:
        print(registro)

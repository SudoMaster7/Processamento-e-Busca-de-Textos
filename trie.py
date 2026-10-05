"""
trie.py
-------
Implementação própria de uma Trie (árvore de prefixos), sem bibliotecas prontas.

Cada nó guarda:
  - filhos: dicionário caractere -> NoTrie (acesso médio O(1) por caractere)
  - fim_de_palavra: indica se o caminho da raiz até este nó forma uma palavra

Esta mesma classe é usada na Parte I (autocomplete) e na Parte II
(mini mecanismo de busca), atendendo ao requisito de reaproveitamento.
"""


import unicodedata


def _chave_alfabetica(caractere):
    """
    Chave de ordenação que coloca letras acentuadas junto da letra base
    (ex.: 'ç' logo após 'c', 'ã' logo após 'a'), em vez de usar a ordem
    pura dos códigos Unicode, que jogaria 'ç' depois do 'z'.
    """
    base = unicodedata.normalize("NFD", caractere)[0]
    return (base, caractere)


class NoTrie:
    """Nó da Trie."""

    __slots__ = ("filhos", "fim_de_palavra")  # reduz o consumo de memória por nó

    def __init__(self):
        self.filhos = {}
        self.fim_de_palavra = False 


class Trie:
    """Árvore de prefixos com inserção, busca exata e busca por prefixo."""

    def __init__(self):
        self.raiz = NoTrie()
        self._total_palavras = 0
        self._total_nos = 1  # a raiz

    # ------------------------------------------------------------------
    # Inserção  -> O(m), m = tamanho da palavra
    # ------------------------------------------------------------------
    def inserir(self, palavra):
        """Insere a palavra. Retorna True se ela era nova, False se já existia."""
        if not palavra:
            return False
        no = self.raiz
        for caractere in palavra:
            if caractere not in no.filhos:
                no.filhos[caractere] = NoTrie()
                self._total_nos += 1
            no = no.filhos[caractere]
        if no.fim_de_palavra:
            return False
        no.fim_de_palavra = True
        self._total_palavras += 1
        return True

    # ------------------------------------------------------------------
    # Navegação auxiliar -> O(m)
    # ------------------------------------------------------------------
    def _localizar_no(self, texto):
        """Desce pela Trie seguindo 'texto'. Retorna o nó final ou None."""
        no = self.raiz
        for caractere in texto:
            no = no.filhos.get(caractere)
            if no is None:
                return None
        return no

    # ------------------------------------------------------------------
    # Busca exata -> O(m)
    # ------------------------------------------------------------------
    def buscar(self, palavra):
        """Retorna True se a palavra completa estiver armazenada."""
        no = self._localizar_no(palavra)
        return no is not None and no.fim_de_palavra

    # ------------------------------------------------------------------
    # Busca por prefixo -> O(p + n), p = tamanho do prefixo,
    # n = nós da subárvore abaixo do prefixo (+ custo de montar as k saídas)
    # ------------------------------------------------------------------
    def buscar_prefixo(self, prefixo, limite=None):
        """
        Retorna, em ordem alfabética, todas as palavras que começam com 'prefixo'.
        'limite' (opcional) interrompe a coleta após N palavras (útil em autocomplete).
        """
        no = self._localizar_no(prefixo)
        if no is None:
            return []
        resultado = []
        self._coletar(no, list(prefixo), resultado, limite)
        return resultado

    def _coletar(self, no, caminho, resultado, limite):
        """Busca em profundidade (DFS) iterativa a partir de 'no'."""
        # Pilha de (nó, caminho). Os filhos são empilhados em ordem reversa
        # para que sejam visitados em ordem alfabética.
        pilha = [(no, "".join(caminho))]
        while pilha:
            atual, texto = pilha.pop()
            if atual.fim_de_palavra:
                resultado.append(texto)
                if limite is not None and len(resultado) >= limite:
                    return
            for caractere in sorted(atual.filhos, key=_chave_alfabetica, reverse=True):
                pilha.append((atual.filhos[caractere], texto + caractere))

    # ------------------------------------------------------------------
    # Informações
    # ------------------------------------------------------------------
    def __len__(self):
        return self._total_palavras

    def __contains__(self, palavra):
        return self.buscar(palavra)

    @property
    def total_nos(self):
        return self._total_nos

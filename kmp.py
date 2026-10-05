"""
kmp.py
------
Algoritmo Knuth-Morris-Pratt (KMP) para busca de uma sequência de caracteres
(padrão) dentro de um texto. Usado na consulta opcional (bônus).

Complexidade: O(n + m), n = tamanho do texto, m = tamanho do padrão.
"""


def tabela_prefixo(padrao):
    """
    Calcula a tabela de falhas (LPS - longest proper prefix which is also suffix).
    lps[i] = tamanho do maior prefixo próprio de padrao[0..i] que também é sufixo.
    Custo O(m).
    """
    lps = [0] * len(padrao)
    comprimento = 0  # tamanho do prefixo-sufixo atual
    i = 1
    while i < len(padrao):
        if padrao[i] == padrao[comprimento]:
            comprimento += 1
            lps[i] = comprimento
            i += 1
        elif comprimento > 0:
            comprimento = lps[comprimento - 1]  # recua sem avançar i
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_buscar(texto, padrao, lps=None):
    """Retorna a lista de posições (índices) onde 'padrao' ocorre em 'texto'."""
    if not padrao:
        return []
    if lps is None:
        lps = tabela_prefixo(padrao)
    posicoes = []
    j = 0  # índice no padrão
    for i, caractere in enumerate(texto):
        while j > 0 and caractere != padrao[j]:
            j = lps[j - 1]  # aproveita o que já casou, sem voltar no texto
        if caractere == padrao[j]:
            j += 1
            if j == len(padrao):
                posicoes.append(i - j + 1)
                j = lps[j - 1]
    return posicoes

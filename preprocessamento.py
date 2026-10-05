"""
preprocessamento.py
-------------------
Etapas de pré-processamento textual:
  1. normalização Unicode (NFC) e conversão para minúsculas
  2. remoção de pontuação (e de números)
  3. tokenização em palavras
  4. remoção de stopwords
  5. (opcional) stemming leve para o português
"""

import os
import re
import unicodedata

# Uma "palavra" é uma sequência de letras (inclui letras acentuadas do português).
# [^\W\d_] = caracteres de palavra que não são dígitos nem sublinhado -> apenas letras.
_PADRAO_TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)


def carregar_stopwords(caminho="stopwords.txt"):
    """Lê o arquivo de stopwords (uma por linha) e devolve um set (busca O(1))."""
    stopwords = set()
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as arq:
            for linha in arq:
                termo = normalizar(linha.strip())
                if termo and not termo.startswith("#"):
                    stopwords.add(termo)
    return stopwords


def normalizar(texto):
    """Normaliza a representação Unicode e converte para minúsculas."""
    return unicodedata.normalize("NFC", texto).lower()


def tokenizar(texto):
    """
    Remove pontuação/números e separa o texto em palavras.
    A expressão regular só captura letras, então pontuação e dígitos
    funcionam como separadores e são descartados.
    """
    return _PADRAO_TOKEN.findall(texto)


def remover_stopwords(tokens, stopwords):
    """Remove stopwords e tokens de uma única letra."""
    return [t for t in tokens if len(t) > 1 and t not in stopwords]


# ----------------------------------------------------------------------
# Stemming opcional (simplificado): remove sufixos comuns do português.
# Não é o algoritmo RSLP completo; é uma versão reduzida baseada em regras
# de remoção de sufixo, aplicadas do mais longo para o mais curto.
# ----------------------------------------------------------------------
_SUFIXOS = sorted([
    "amentos", "imentos", "amento", "imento", "adoras", "adores", "ações",
    "adora", "ador", "ação", "ância", "ência", "mente", "idades", "idade",
    "ismos", "ismo", "istas", "ista", "ivos", "ivas", "ivo", "iva",
    "ais", "eis", "óis", "ões", "ães", "al", "es", "as", "os", "s",
    "o", "a", "e",  # vogal temática final: unifica singular/plural (algoritmo/algoritmos)
], key=len, reverse=True)


def stem(palavra):
    """Remove o sufixo mais longo aplicável, preservando um radical mínimo de 3 letras."""
    for sufixo in _SUFIXOS:
        if palavra.endswith(sufixo) and len(palavra) - len(sufixo) >= 3:
            return palavra[: -len(sufixo)]
    return palavra


def preprocessar(texto, stopwords, usar_stemming=False):
    """Pipeline completo: minúsculas -> pontuação -> tokens -> stopwords (-> stemming)."""
    tokens = tokenizar(normalizar(texto))
    tokens = remover_stopwords(tokens, stopwords)
    if usar_stemming:
        tokens = [stem(t) for t in tokens]
    return tokens

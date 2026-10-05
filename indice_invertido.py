"""
indice_invertido.py
-------------------
Índice invertido no formato  termo -> {documentos}.

A estrutura é um dict do Python, ou seja, uma TABELA HASH:
  - a chave (termo) passa por uma função hash, que indica a posição na tabela;
  - a busca, inserção e atualização custam O(1) em média;
  - colisões (termos diferentes com mesma posição) são tratadas internamente
    pelo Python via endereçamento aberto (sondagem).

Além do conjunto de documentos, guardamos a frequência do termo em cada
documento (termo -> {documento: frequência}), o que permite ordenar resultados.
"""


class IndiceInvertido:

    def __init__(self):
        # termo -> {nome_documento: frequência}
        self._indice = {}

    def adicionar_documento(self, nome_documento, tokens):
        """Adiciona todos os tokens de um documento. O(t), t = nº de tokens."""
        for termo in tokens:
            postagens = self._indice.get(termo)          # O(1) médio (hash)
            if postagens is None:
                postagens = {}
                self._indice[termo] = postagens          # O(1) médio (hash)
            postagens[nome_documento] = postagens.get(nome_documento, 0) + 1

    def documentos_do_termo(self, termo):
        """Conjunto de documentos em que o termo aparece. O(1) médio + O(d) para copiar."""
        return set(self._indice.get(termo, {}))

    def frequencias(self, termo):
        """Dicionário {documento: frequência} do termo."""
        return dict(self._indice.get(termo, {}))

    def vocabulario(self):
        """Conjunto de termos distintos."""
        return set(self._indice.keys())

    def __contains__(self, termo):
        return termo in self._indice

    def __len__(self):
        return len(self._indice)

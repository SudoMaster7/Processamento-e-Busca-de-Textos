"""
main.py  —  PARTE II
--------------------
Mini mecanismo de busca em arquivos .txt.

Fluxo:
  pasta documentos/ -> pré-processamento -> índice invertido (hash)
                    -> vocabulário -> Trie (reaproveitada da Parte I)

Uso:
    python main.py                    (pasta padrão: documentos/)
    python main.py outra_pasta        (outra pasta)
    python main.py --stemming         (ativa o stemming opcional)
"""

import os
import sys
import time

from trie import Trie
from indice_invertido import IndiceInvertido
from preprocessamento import carregar_stopwords, preprocessar, normalizar
from kmp import kmp_buscar, tabela_prefixo


class MecanismoBusca:

    def __init__(self, pasta="documentos", arquivo_stopwords="stopwords.txt",
                 usar_stemming=False):
        self.pasta = pasta
        self.usar_stemming = usar_stemming
        self.stopwords = carregar_stopwords(arquivo_stopwords)
        self.trie = Trie()
        self.indice = IndiceInvertido()
        self.documentos = {}          # nome -> texto original
        self.textos_normalizados = {} # nome -> texto em minúsculas (usado pelo KMP)
        self.tokens_por_doc = {}      # nome -> lista de tokens
        self.total_palavras = 0
        self.tempos = {}
        self.historico = []           # (tipo, consulta, tempo_ms)

    # ------------------------------------------------------------------
    # Construção
    # ------------------------------------------------------------------
    def carregar_documentos(self):
        """Lê TODOS os .txt da pasta (nomes não fixos no código)."""
        if not os.path.isdir(self.pasta):
            raise FileNotFoundError(f"Pasta '{self.pasta}' não encontrada.")
        arquivos = sorted(a for a in os.listdir(self.pasta) if a.lower().endswith(".txt"))
        for nome in arquivos:
            with open(os.path.join(self.pasta, nome), encoding="utf-8") as arq:
                self.documentos[nome] = arq.read()
                self.textos_normalizados[nome] = normalizar(self.documentos[nome])

    def preprocessar_documentos(self):
        inicio = time.perf_counter()
        for nome, texto in self.documentos.items():
            tokens = preprocessar(texto, self.stopwords, self.usar_stemming)
            self.tokens_por_doc[nome] = tokens
            self.total_palavras += len(tokens)
        self.tempos["preprocessamento"] = time.perf_counter() - inicio

    def construir_indice(self):
        inicio = time.perf_counter()
        for nome, tokens in self.tokens_por_doc.items():
            self.indice.adicionar_documento(nome, tokens)
        self.tempos["indice"] = time.perf_counter() - inicio

    def construir_trie(self):
        """Insere o vocabulário (termos distintos) na Trie."""
        inicio = time.perf_counter()
        for termo in self.indice.vocabulario():
            self.trie.inserir(termo)
        self.tempos["trie"] = time.perf_counter() - inicio

    def construir(self):
        self.carregar_documentos()
        self.preprocessar_documentos()
        self.construir_indice()
        self.construir_trie()

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def _registrar(self, tipo, consulta, inicio):
        tempo_ms = (time.perf_counter() - inicio) * 1000
        self.historico.append((tipo, consulta, tempo_ms))
        return tempo_ms

    def buscar_palavra(self, entrada):
        """Consulta exata no índice invertido (hash)."""
        inicio = time.perf_counter()
        tokens = preprocessar(entrada, set(), self.usar_stemming)
        termo = tokens[0] if tokens else ""
        freq = self.indice.frequencias(termo)
        ordenado = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
        tempo = self._registrar("palavra", entrada, inicio)
        return termo, ordenado, tempo

    def buscar_prefixo(self, entrada):
        """Trie -> termos com o prefixo; índice invertido -> documentos de cada termo."""
        inicio = time.perf_counter()
        prefixo = normalizar(entrada.strip())
        termos = self.trie.buscar_prefixo(prefixo)
        resultado = [(t, sorted(self.indice.documentos_do_termo(t))) for t in termos]
        tempo = self._registrar("prefixo", entrada, inicio)
        return resultado, tempo

    def buscar_sequencia(self, entrada):
        """KMP diretamente no conteúdo original (em minúsculas) de cada documento."""
        inicio = time.perf_counter()
        padrao = normalizar(entrada)
        lps = tabela_prefixo(padrao) if padrao else []
        resultado = []
        for nome, texto in self.textos_normalizados.items():
            posicoes = kmp_buscar(texto, padrao, lps)
            if posicoes:
                original = self.documentos[nome]
                resultado.append((nome, len(posicoes), self._trecho(original, posicoes[0], len(padrao))))
        resultado.sort(key=lambda x: (-x[1], x[0]))
        tempo = self._registrar("sequência", entrada, inicio)
        return resultado, tempo

    @staticmethod
    def _trecho(texto, pos, tamanho, margem=30):
        ini, fim = max(0, pos - margem), min(len(texto), pos + tamanho + margem)
        return ("..." if ini else "") + texto[ini:fim].replace("\n", " ") + ("..." if fim < len(texto) else "")


# ----------------------------------------------------------------------
# Interface de texto
# ----------------------------------------------------------------------
def cabecalho(mb):
    print("\n" + "=" * 48)
    print("        SISTEMA DE BUSCA EM DOCUMENTOS")
    print("=" * 48)
    print(f"Documentos processados: {len(mb.documentos)}")
    print(f"Total de palavras: {mb.total_palavras}")
    print(f"Termos distintos: {len(mb.indice)}\n")
    print("1 - Buscar palavra")
    print("2 - Buscar por prefixo")
    print("3 - Buscar sequência nos documentos (KMP)")
    print("4 - Listar documentos")
    print("5 - Exibir estatísticas")
    print("6 - Sair")


def exibir_estatisticas(mb):
    t = mb.tempos
    print("\n--- ESTATÍSTICAS ---")
    print(f"Documentos processados ............ {len(mb.documentos)}")
    print(f"Total de palavras (pós-tokenização) {mb.total_palavras}")
    print(f"Termos distintos (vocabulário) .... {len(mb.indice)}")
    print(f"Palavras armazenadas na Trie ...... {len(mb.trie)}")
    print(f"Nós da Trie ....................... {mb.trie.total_nos}")
    print(f"Stemming .......................... {'ativado' if mb.usar_stemming else 'desativado'}")
    print(f"Tempo de pré-processamento ........ {t['preprocessamento']*1000:.2f} ms")
    print(f"Tempo de construção do índice ..... {t['indice']*1000:.2f} ms")
    print(f"Tempo de construção da Trie ....... {t['trie']*1000:.2f} ms")
    if mb.historico:
        print("\nConsultas realizadas:")
        for tipo, consulta, tempo in mb.historico:
            print(f"  [{tipo:9}] '{consulta}' -> {tempo:.4f} ms")
    else:
        print("\nNenhuma consulta realizada ainda.")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    usar_stemming = "--stemming" in sys.argv
    pasta = args[0] if args else "documentos"

    mb = MecanismoBusca(pasta=pasta, usar_stemming=usar_stemming)
    mb.construir()

    while True:
        cabecalho(mb)
        try:
            opcao = input("\nEscolha uma opção: ").strip()
        except EOFError:
            break

        if opcao == "1":
            entrada = input("Digite a palavra: ")
            termo, docs, tempo = mb.buscar_palavra(entrada)
            if docs:
                print(f"\nTermo '{termo}' encontrado em {len(docs)} arquivo(s):")
                for nome, freq in docs:
                    print(f"  - {nome} ({freq} ocorrência(s))")
            else:
                print(f"\nTermo '{termo}' não encontrado em nenhum documento.")
            print(f"Tempo da consulta: {tempo:.4f} ms")

        elif opcao == "2":
            entrada = input("Digite o prefixo: ")
            resultado, tempo = mb.buscar_prefixo(entrada)
            if resultado:
                print(f"\nPalavras encontradas ({len(resultado)}):")
                for termo, docs in resultado:
                    print(f"  {termo:<22} -> {', '.join(docs)}")
            else:
                print("\nNenhuma palavra encontrada com esse prefixo.")
            print(f"Tempo da consulta: {tempo:.4f} ms")

        elif opcao == "3":
            entrada = input("Digite a sequência: ")
            resultado, tempo = mb.buscar_sequencia(entrada)
            if resultado:
                print(f"\nSequência encontrada em {len(resultado)} arquivo(s):")
                for nome, qtd, trecho in resultado:
                    print(f"  - {nome} ({qtd}x)  {trecho}")
            else:
                print("\nSequência não encontrada.")
            print(f"Tempo da consulta: {tempo:.4f} ms")

        elif opcao == "4":
            print("\nDocumentos indexados:")
            for i, nome in enumerate(mb.documentos, 1):
                print(f"  D{i}: {nome} ({len(mb.tokens_por_doc[nome])} palavras)")

        elif opcao == "5":
            exibir_estatisticas(mb)

        elif opcao == "6":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

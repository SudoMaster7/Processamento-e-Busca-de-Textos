"""
autocomplete.py  —  PARTE I
---------------------------
Sistema de autocomplete de palavras usando a Trie implementada em trie.py.

Uso:
    python autocomplete.py                 (carrega palavras.txt, se existir)
    python autocomplete.py minhas.txt      (carrega outro arquivo de palavras)
"""

import os
import sys
import time

from trie import Trie
from preprocessamento import normalizar

PALAVRAS_EXEMPLO = [
    "computador", "computação", "computacional", "compilador",
    "complexidade", "programação", "processador", "processamento",
]


def carregar_palavras(trie, caminho):
    """Insere na Trie cada palavra do arquivo (uma por linha)."""
    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            palavra = normalizar(linha.strip())
            if palavra:
                trie.inserir(palavra)


def ler_palavra(mensagem):
    """Lê e normaliza a entrada do usuário (minúsculas, Unicode NFC)."""
    return normalizar(input(mensagem).strip())


def menu(trie):
    while True:
        print("\n" + "=" * 36)
        print("       AUTOCOMPLETE COM TRIE")
        print("=" * 36)
        print(f"Palavras cadastradas: {len(trie)}\n")
        print("1 - Buscar palavra")
        print("2 - Buscar por prefixo")
        print("3 - Inserir nova palavra")
        print("4 - Sair")
        try:
            opcao = input("\nEscolha uma opção: ").strip()
        except EOFError:
            break

        if opcao == "1":
            palavra = ler_palavra("Digite a palavra: ")
            inicio = time.perf_counter()
            existe = trie.buscar(palavra)
            tempo = (time.perf_counter() - inicio) * 1000
            status = "EXISTE" if existe else "NÃO existe"
            print(f"'{palavra}' {status} na Trie.  ({tempo:.4f} ms)")

        elif opcao == "2":
            prefixo = ler_palavra("Digite o prefixo: ")
            inicio = time.perf_counter()
            palavras = trie.buscar_prefixo(prefixo)
            tempo = (time.perf_counter() - inicio) * 1000
            if palavras:
                print(f"\nPalavras encontradas ({len(palavras)}):")
                for p in palavras:
                    print(f"  {p}")
            else:
                print("Nenhuma palavra encontrada com esse prefixo.")
            print(f"Tempo da consulta: {tempo:.4f} ms")

        elif opcao == "3":
            palavra = ler_palavra("Nova palavra: ")
            if not palavra.isalpha():
                print("Palavra inválida (use apenas letras).")
            elif trie.inserir(palavra):
                print(f"'{palavra}' inserida com sucesso.")
            else:
                print(f"'{palavra}' já estava cadastrada.")

        elif opcao == "4":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


def main():
    trie = Trie()
    caminho = sys.argv[1] if len(sys.argv) > 1 else "palavras.txt"
    if os.path.exists(caminho):
        inicio = time.perf_counter()
        carregar_palavras(trie, caminho)
        tempo = (time.perf_counter() - inicio) * 1000
        print(f"{len(trie)} palavras carregadas de '{caminho}' em {tempo:.2f} ms "
              f"({trie.total_nos} nós na Trie).")
    for p in PALAVRAS_EXEMPLO:  # garante as palavras do enunciado
        trie.inserir(p)
    menu(trie)


if __name__ == "__main__":
    main()

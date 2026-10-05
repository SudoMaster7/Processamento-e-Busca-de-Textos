"""
experimento_escala.py
---------------------
Experimento empírico para relacionar os tempos medidos com a análise
assintótica (Unidade 1). O corpus da pasta documentos/ é replicado
k vezes (k = 1, 2, 4, 8, 16, 32) e, para cada tamanho, medimos:

  - tempo de pré-processamento   (esperado: cresce linearmente com o texto)
  - tempo do índice invertido    (esperado: linear no nº de tokens)
  - tempo da Trie                (depende do vocabulário, que NÃO cresce
                                  quando o texto é apenas replicado)
  - tempo de busca exata (hash)  (esperado: ~constante)
  - tempo de busca por prefixo   (esperado: ~constante, depende do prefixo)

Uso:  python experimento_escala.py
"""

import time

from main import MecanismoBusca


def medir(funcao, repeticoes=200):
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        funcao()
    return (time.perf_counter() - inicio) / repeticoes * 1000  # ms


def main():
    base = MecanismoBusca()
    base.carregar_documentos()

    print(f"{'k':>3} | {'tokens':>8} | {'pré-proc (ms)':>13} | {'índice (ms)':>11} | "
          f"{'Trie (ms)':>9} | {'busca (ms)':>10} | {'prefixo (ms)':>12}")
    print("-" * 86)
    for k in (1, 2, 4, 8, 16, 32):
        mb = MecanismoBusca()
        # replica cada documento k vezes, como se fossem arquivos diferentes
        for nome, texto in base.documentos.items():
            for i in range(k):
                mb.documentos[f"{i}_{nome}"] = texto
        mb.preprocessar_documentos()
        mb.construir_indice()
        mb.construir_trie()
        t_busca = medir(lambda: mb.indice.frequencias("algoritmos"))
        t_pref = medir(lambda: mb.trie.buscar_prefixo("comp"))
        print(f"{k:>3} | {mb.total_palavras:>8} | {mb.tempos['preprocessamento']*1000:>13.2f} | "
              f"{mb.tempos['indice']*1000:>11.2f} | {mb.tempos['trie']*1000:>9.2f} | "
              f"{t_busca:>10.4f} | {t_pref:>12.4f}")


if __name__ == "__main__":
    main()

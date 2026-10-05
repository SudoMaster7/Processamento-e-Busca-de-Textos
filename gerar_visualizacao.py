"""
gerar_visualizacao.py
---------------------
Embute em visualizacao.html o conteúdo atual de documentos/, palavras.txt e
stopwords.txt, para que a página funcione aberta direto do disco (sem servidor).

Rode novamente sempre que adicionar ou alterar algum desses arquivos:
    python gerar_visualizacao.py
"""

import json
import os
import re

PAGINA = "visualizacao.html"


def ler(caminho):
    with open(caminho, encoding="utf-8") as arq:
        return arq.read()


def main():
    documentos = {
        nome: ler(os.path.join("documentos", nome))
        for nome in sorted(os.listdir("documentos"))
        if nome.lower().endswith(".txt")
    }
    dados = {
        "documentos": documentos,
        "palavras": ler("palavras.txt") if os.path.exists("palavras.txt") else "",
        "stopwords": ler("stopwords.txt") if os.path.exists("stopwords.txt") else "",
    }
    # "</" escapado evita que um texto feche a tag <script> por engano
    json_dados = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")

    html = ler(PAGINA)
    html, trocas = re.subn(
        r"/\*DADOS_INICIO\*/.*?/\*DADOS_FIM\*/",
        lambda _: "/*DADOS_INICIO*/" + json_dados + "/*DADOS_FIM*/",
        html,
        count=1,
        flags=re.DOTALL,
    )
    if not trocas:
        raise SystemExit(f"Marcadores de dados não encontrados em {PAGINA}.")
    with open(PAGINA, "w", encoding="utf-8") as arq:
        arq.write(html)
    print(f"{PAGINA} atualizado: {len(documentos)} documentos embutidos.")


if __name__ == "__main__":
    main()

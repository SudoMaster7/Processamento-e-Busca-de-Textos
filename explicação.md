# Roteiro para apresentação do projeto

## 1. Apresentação inicial

Você pode começar assim:

> “O projeto é um sistema de processamento e busca de textos. Ele possui duas partes principais: a primeira implementa uma Trie para autocomplete e busca por prefixo; a segunda reaproveita essa Trie em um mecanismo de busca sobre vários documentos. Também foi implementado um índice invertido baseado em tabela hash para localizar palavras rapidamente e o algoritmo KMP para buscar sequências de caracteres.”

O projeto está organizado principalmente nos seguintes arquivos:

- `preprocessamento.py`
- `trie.py`
- `indice_invertido.py`
- `kmp.py`
- `main.py`
- `experimento_escala.py`

---

# 2. Objetivo do sistema

Explique o objetivo geral:

> “O sistema recebe vários arquivos `.txt`, processa o conteúdo desses arquivos, cria estruturas eficientes para consulta e permite fazer três tipos principais de busca: busca exata por palavra, busca por prefixo e busca por sequência de caracteres.”

Exemplo:

```text
Documentos:
- artigo1.txt
- artigo2.txt
- artigo3.txt
```

O programa lê esses documentos e constrói uma espécie de banco de dados em memória para responder às consultas.

---

# 3. Fluxo geral do programa

Mostre este fluxo:

```text
Arquivos .txt
     ↓
Leitura dos documentos
     ↓
Pré-processamento
     ↓
Tokens limpos
     ↓
Índice invertido baseado em hash
     ↓
Vocabulário inserido na Trie
     ↓
Consultas do usuário
```

No arquivo `main.py`, esse processo é realizado por:

```python
def construir(self):
    self.carregar_documentos()
    self.preprocessar_documentos()
    self.construir_indice()
    self.construir_trie()
```

Você pode dizer:

> “Primeiro o programa carrega os documentos. Depois faz o pré-processamento, constrói o índice invertido e, por fim, insere o vocabulário na Trie.”

---

# 4. Pré-processamento dos textos

O pré-processamento está em `preprocessamento.py`.

Ele executa estas etapas:

```text
Texto original
     ↓
Normalização Unicode
     ↓
Conversão para minúsculas
     ↓
Remoção de pontuação e números
     ↓
Tokenização
     ↓
Remoção de stopwords
     ↓
Stemming opcional
```

## 4.1 Normalização

A função `normalizar` converte o texto para uma forma Unicode consistente e para letras minúsculas:

```python
def normalizar(texto):
    return unicodedata.normalize("NFC", texto).lower()
```

Assim, por exemplo:

```text
"ÁLGORITMOS"
```

vira:

```text
"algoritmos"
```

Isso faz com que `"Algoritmos"` e `"algoritmos"` sejam tratados como o mesmo termo.

## 4.2 Tokenização

A função `tokenizar` separa o texto em palavras.

A expressão regular utilizada é:

```python
r"[^\W\d_]+"
```

Ela captura sequências de letras, inclusive letras acentuadas, e ignora:

- pontuação;
- números;
- sublinhado.

Exemplo:

```text
"Algoritmos, dados e 2024!"
```

pode gerar:

```python
["algoritmos", "dados", "e"]
```

## 4.3 Stopwords

Stopwords são palavras muito comuns que normalmente não ajudam muito na busca, como:

```text
de, da, do, e, o, a, em, para
```

Elas são carregadas em um `set`, que permite consultas rápidas:

```python
termo in stopwords
```

A busca em um conjunto possui custo médio `O(1)`.

## 4.4 Stemming

O stemming é opcional e remove alguns sufixos.

Por exemplo, palavras como:

```text
algoritmo
algoritmos
```

podem ser aproximadas para um mesmo radical.

É importante explicar:

> “O stemming implementado é simplificado. Ele não é o algoritmo completo RSLP; é um conjunto de regras próprias que remove sufixos comuns da língua portuguesa.”

O usuário pode ativá-lo com:

```bash
python main.py --stemming
```

---

# 5. Parte I: Trie e autocomplete

A Trie está implementada em `trie.py`.

## 5.1 O que é uma Trie?

Você pode explicar assim:

> “A Trie é uma árvore de prefixos. Cada caminho da raiz até um nó representa uma palavra. Cada nó guarda seus filhos, que são os próximos caracteres possíveis.”

Exemplo para as palavras:

```text
casa
cama
carro
```

A estrutura começa compartilhando o prefixo `ca`:

```text
       c
       |
       a
     / | \
    s  m  r
    |  |  |
    a  a  r
          |
          o
```

As palavras que possuem o mesmo prefixo reutilizam os mesmos nós iniciais.

## 5.2 Estrutura de cada nó

Cada nó possui:

```python
self.filhos = {}
self.fim_de_palavra = False
```

- `filhos` guarda os próximos caracteres;
- `fim_de_palavra` informa se aquele ponto representa uma palavra completa.

Por exemplo, em `casa`, o nó final de `casa` possui:

```python
fim_de_palavra = True
```

Isso é necessário porque uma palavra também pode ser prefixo de outra.

Exemplo:

```text
car
carro
```

O nó de `car` precisa indicar que `car` já é uma palavra, mesmo tendo um filho para continuar em `carro`.

## 5.3 Inserção

Para inserir uma palavra, o programa percorre seus caracteres:

```text
c → a → s → a
```

Se algum nó ainda não existir, ele é criado.

A complexidade é:

```text
O(m)
```

onde `m` é o tamanho da palavra.

A busca exata também custa `O(m)`, porque percorre os caracteres da palavra.

## 5.4 Busca por prefixo

Para buscar o prefixo `"ca"`:

1. o programa percorre a Trie até chegar ao nó de `"ca"`;
2. a partir desse nó, percorre todos os descendentes;
3. coleta as palavras encontradas.

Essa coleta é feita por uma busca em profundidade, ou DFS, usando uma pilha.

Exemplo:

```text
Prefixo pesquisado: ca

Resultado:
- cama
- casa
- carro
```

A Trie é mais adequada que uma lista comum porque não precisa comparar o prefixo completo com todas as palavras.

---

# 6. Parte II: índice invertido

O índice invertido está em `indice_invertido.py`.

## 6.1 O que é uma tabela hash?

Uma tabela hash armazena dados no formato:

```text
chave → valor
```

No Python, o tipo `dict` é implementado como uma tabela hash.

Exemplo:

```python
tabela = {
    "python": 3,
    "algoritmo": 5
}
```

Quando buscamos uma chave, o Python calcula uma função hash para localizar rapidamente o valor.

A busca, inserção e atualização possuem custo médio:

```text
O(1)
```

## 6.2 O que é um índice invertido?

Um índice invertido associa cada termo aos documentos onde ele aparece.

Exemplo:

```text
python     → documento1.txt, documento3.txt
algoritmo  → documento1.txt, documento2.txt
```

No seu projeto, além dos documentos, também é armazenada a frequência:

```python
{
    "algoritmos": {
        "documento1.txt": 2,
        "documento2.txt": 1
    }
}
```

Isso significa:

> A palavra `algoritmos` aparece duas vezes no primeiro documento e uma vez no segundo.

A estrutura utilizada é:

```text
termo → documento → frequência
```

Ou seja, existem dois dicionários:

```python
self._indice[termo][nome_documento] = frequencia
```

## 6.3 Construção do índice

Para cada token de cada documento, o sistema:

1. verifica se o termo já está no índice;
2. cria uma entrada caso ainda não exista;
3. registra o documento;
4. incrementa a frequência.

Exemplo de documento:

```text
python python algoritmos
```

O índice resultará em:

```python
{
    "python": {
        "documento1.txt": 2
    },
    "algoritmos": {
        "documento1.txt": 1
    }
}
```

## 6.4 Por que usar o índice invertido?

Sem o índice, a cada pesquisa seria necessário abrir e examinar todos os documentos.

Com o índice, a busca por uma palavra é direta:

```python
indice.frequencias("python")
```

Resultado:

```python
{
    "documento1.txt": 2,
    "documento3.txt": 1
}
```

Depois, os documentos são ordenados pela frequência do termo.

---

# 7. Como a busca por palavra funciona

Quando o usuário escolhe:

```text
1 - Buscar palavra
```

o sistema:

1. recebe a consulta;
2. aplica o mesmo pré-processamento;
3. consulta o índice invertido;
4. ordena os resultados pela frequência;
5. exibe os documentos encontrados.

Exemplo:

```text
Consulta: algoritmos
```

Resultado:

```text
Termo encontrado em 2 arquivos:
- documento1.txt (3 ocorrências)
- documento2.txt (1 ocorrência)
```

A consulta usa principalmente a tabela hash, então a localização do termo possui custo médio `O(1)`, sem considerar a quantidade de documentos retornados e a ordenação.

---

# 8. Como a busca por prefixo funciona

Quando o usuário escolhe:

```text
2 - Buscar por prefixo
```

o sistema combina a Trie com o índice invertido.

Fluxo:

```text
Prefixo digitado
     ↓
Trie encontra os termos correspondentes
     ↓
Índice invertido localiza os documentos
     ↓
Resultado final
```

Exemplo:

```text
Prefixo: comp
```

A Trie pode encontrar:

```text
computador
computação
complexidade
```

Depois, para cada termo, o índice invertido informa os documentos correspondentes.

Essa divisão de responsabilidades é importante:

- a Trie resolve o problema do prefixo;
- o índice invertido resolve o problema dos documentos.

---

# 9. Busca por sequência usando KMP

O algoritmo KMP está em `kmp.py`.

Ele é utilizado quando o usuário escolhe:

```text
3 - Buscar sequência nos documentos (KMP)
```

## 9.1 O que o KMP faz?

O KMP procura uma sequência de caracteres dentro de um texto.

Exemplo:

```text
Texto:   "estruturas de dados"
Padrão:  "dados"
```

O algoritmo encontra a posição onde `"dados"` aparece.

## 9.2 Diferença para a busca por palavra

A busca por palavra usa o índice invertido e procura um termo já processado.

A busca por sequência procura uma sequência literal dentro do texto normalizado.

Exemplos:

```text
"estrutura de dados"
"busca em profundidade"
"algoritmo de ordenação"
```

Podem ser pesquisados como sequências.

## 9.3 Tabela LPS

O KMP utiliza uma tabela chamada `LPS`:

```text
Longest Proper Prefix which is also Suffix
```

Em português:

> maior prefixo próprio que também é sufixo.

Essa tabela informa quanto do padrão já pode ser reaproveitado quando ocorre uma falha na comparação.

A vantagem é que o algoritmo não precisa voltar para trás no texto.

A complexidade é:

```text
O(n + m)
```

onde:

- `n` é o tamanho do texto;
- `m` é o tamanho do padrão.

No sistema, o KMP é executado para cada documento e retorna as posições encontradas.

---

# 10. Diferença entre as três buscas

Explique esta tabela:

| Tipo de busca | Estrutura principal | Objetivo |
|---|---|---|
| Palavra exata | Índice invertido/hash | Encontrar documentos que contêm um termo |
| Prefixo | Trie + índice invertido | Encontrar palavras que começam com determinado prefixo |
| Sequência | KMP | Encontrar uma sequência de caracteres no texto |

Exemplo:

```text
Busca por palavra: "algoritmos"
Busca por prefixo: "algo"
Busca por sequência: "algoritmos são importantes"
```

---

# 11. Complexidade dos algoritmos

Você pode apresentar assim:

| Operação | Complexidade aproximada |
|---|---|
| Inserir palavra na Trie | `O(m)` |
| Buscar palavra na Trie | `O(m)` |
| Buscar prefixo na Trie | `O(p + n)` mais o custo das saídas |
| Buscar termo no índice hash | `O(1)` médio |
| Inserir tokens no índice | `O(t)` para `t` tokens |
| Construir tabela LPS do KMP | `O(m)` |
| Buscar sequência com KMP | `O(n + m)` |
| Pré-processar texto | Linear em relação ao tamanho do texto |

Onde:

- `m` é o tamanho da palavra ou padrão;
- `p` é o tamanho do prefixo;
- `n` é o tamanho do texto ou da subárvore percorrida;
- `t` é a quantidade de tokens.

Uma observação importante:

> “O `O(1)` da tabela hash é uma média. Em situações de colisão, o comportamento pode ser diferente, mas o Python trata as colisões internamente.”

---

# 12. Estatísticas e medição de tempo

O sistema mede o tempo de:

- pré-processamento;
- construção do índice;
- construção da Trie;
- consultas realizadas.

As medições são feitas com:

```python
time.perf_counter()
```

O programa também informa:

- número de documentos;
- total de palavras;
- quantidade de termos distintos;
- quantidade de palavras na Trie;
- quantidade de nós da Trie;
- estado do stemming;
- histórico das consultas.

Isso permite comparar o comportamento prático com a análise teórica de complexidade.

---

# 13. Experimento de escala

O experimento está em `experimento_escala.py`.

Ele replica os documentos várias vezes:

```text
k = 1, 2, 4, 8, 16, 32
```

Para cada tamanho, mede:

- tempo de pré-processamento;
- tempo de construção do índice;
- tempo de construção da Trie;
- tempo de busca exata;
- tempo de busca por prefixo.

A expectativa é:

- o pré-processamento crescer conforme aumenta o texto;
- a construção do índice crescer conforme aumenta a quantidade de tokens;
- a busca exata por hash permanecer aproximadamente constante;
- a busca por prefixo depender principalmente do prefixo e dos resultados encontrados;
- a Trie não crescer tanto quando os mesmos textos são apenas replicados, pois o vocabulário continua parecido.

Você pode dizer:

> “Esse experimento compara a análise assintótica com os tempos observados na prática.”

---

# 14. Demonstração prática sugerida

Durante a apresentação, faça esta sequência:

## Etapa 1 — Iniciar o programa

```bash
python main.py
```

Mostre que o sistema informa:

```text
Documentos processados
Total de palavras
Termos distintos
```

## Etapa 2 — Busca exata

Pesquise uma palavra que exista:

```text
algoritmos
```

Explique que o índice invertido retorna os documentos e as frequências.

Depois pesquise uma palavra inexistente e mostre que o sistema informa que ela não foi encontrada.

## Etapa 3 — Busca por prefixo

Pesquise:

```text
comp
```

Explique que:

1. a Trie encontra palavras como `computação`, `complexidade` etc.;
2. o índice invertido localiza os documentos dessas palavras.

## Etapa 4 — Busca por sequência

Pesquise uma frase curta presente em algum documento.

Explique que essa consulta usa o KMP e não apenas o índice de palavras.

## Etapa 5 — Stemming

Execute:

```bash
python main.py --stemming
```

Explique que o stemming tenta agrupar palavras com terminações semelhantes.

## Etapa 6 — Estatísticas

Escolha:

```text
5 - Exibir estatísticas
```

Mostre os tempos e as quantidades calculadas.

---

# 15. Perguntas que o professor pode fazer

## Por que usar uma Trie?

Resposta:

> “Porque a Trie é especializada em prefixos. A busca por uma palavra e principalmente a busca por autocomplete dependem do tamanho da palavra ou do prefixo, e não da quantidade total de palavras armazenadas.”

## Por que usar um índice invertido?

Resposta:

> “Porque ele evita percorrer todos os documentos a cada busca. A palavra é usada como chave e os documentos aparecem associados a ela.”

## Por que o índice é chamado de invertido?

Resposta:

> “Porque ele inverte a organização tradicional. Em vez de documento apontando para palavras, temos palavra apontando para documentos.”

## Por que usar um `dict`?

Resposta:

> “Porque o `dict` do Python utiliza uma tabela hash, permitindo busca, inserção e atualização em tempo médio constante.”

## O que acontece com palavras repetidas?

Resposta:

> “A frequência do termo no documento é incrementada. Isso permite ordenar os resultados por quantidade de ocorrências.”

## Qual é a função da DFS?

Resposta:

> “A DFS percorre a subárvore da Trie depois que o prefixo é localizado, coletando todas as palavras que continuam a partir daquele prefixo.”

## Por que usar KMP?

Resposta:

> “Porque o KMP busca uma sequência de caracteres em tempo linear, `O(n + m)`, evitando comparações desnecessárias quando há falhas parciais no padrão.”

## O que são stopwords?

Resposta:

> “São palavras muito frequentes e pouco informativas para a busca, como artigos, preposições e conjunções. Elas são removidas para reduzir ruído e o tamanho do índice.”

## O que é stemming?

Resposta:

> “É uma técnica que reduz palavras para uma forma aproximada de seu radical. Neste projeto, foi implementada uma versão simplificada baseada na remoção de sufixos.”

## O que acontece se houver colisão na tabela hash?

Resposta:

> “O próprio Python trata as colisões internamente. O programa utiliza o `dict`, então não precisa implementar manualmente a sondagem ou outra técnica de resolução.”

---

# 16. Encerramento da apresentação

Finalize com:

> “O projeto combina diferentes estruturas e algoritmos, cada um com uma função específica. O pré-processamento prepara os textos, o índice invertido permite localizar documentos rapidamente, a Trie resolve buscas por prefixo e autocomplete, e o KMP trata buscas por sequências. Dessa forma, o sistema demonstra na prática como estruturas de dados e análise de complexidade podem ser aplicadas a um mecanismo de busca.”

## Resumo para memorizar

```text
Pré-processamento → limpa os textos
Índice invertido  → palavra para documentos
Tabela hash       → acesso rápido
Trie              → prefixos e autocomplete
DFS               → percorre a Trie
KMP               → busca sequências
Experimento       → compara teoria e prática
```
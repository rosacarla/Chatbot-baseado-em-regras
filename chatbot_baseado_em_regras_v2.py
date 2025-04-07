# -*- coding: utf-8 -*-
"""Chatbot_baseado_em_regras_v2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jnE_erytgSby0UP4NnEP-BosxP4k0TVE

> # CHATBOT DE ATENDIMENTO AO CLIENTE BASEADO EM REGRAS
> CURSO: Tecnólogo em Inteligência Artificial Aplicada  
> DISCIPLINA: Agentes Conversacionais  
> AUTOR: Carla Edila Silveira  
> OBJETIVO: construir um chatbot com emprego de técnicas mais simples de desenvolvimento  
> MELHORIA: inclusão das intenções de 'endereço', 'delivery' e 'reserva' na base de dados do restaurante  
> DATA: 07/04/2025
_______________________________________________________________________

<img src="https://i.postimg.cc/xC2N8ntY/CHATBOT-BASEADO-EM-REGRAS.jpg" height=364 width=940>

> ## 1. O que é um CHATBOT BASEADO EM REGRAS?
> <p align="justify">Este é um tipo de chatbot mais simples, composto por um dataset com respostas pré-definidas e uma série de regras para encontrar as respostas (ou intenções) no dataset.</p>
> <p align="justify">Embora apresente certas limitações, podem ser muito eficientes e produtivos se houver regras bem definidas e um dataset substancial com respostas.</p>

> ## 2. Qual é o contexto do chatbot deste projeto?
> <p align="justify">Como contextualização, será desenvolvido um chatbot de interação com clientes de um restaurante. O objetivo do chatbot é auxiliar o cliente a encontrar informações desejadas sem a necessidade de navegar por vários links do site.</p>

> ## 3. Quais ferramentas e técnicas serão adotados?
>*   **NLTK** - toolkit mais famoso de Processamento de Linguagem Natural em Python
>*   **Expressões Regulares** - pacote de regex do Python para otimizar a busca de padrões
>*   **WordNet** - banco de dados léxico e semântico, disponível em diversos idiomas

> ## 4. Construção do chatbot
> O modo de operação do chatbot é o seguinte:
>1.   Recebe **entrada** do usuário.
>2.   Procura **palavras-chave** na entrada do usuário.
>3.   Define a **intenção associada** à entrada.
>4.   Obtém a **resposta baseada na intenção** definida.
>5.   Mostra a **resposta** ao usuário.  

>Para isso, é necessário uma **tabela que associe as palavras-chave desejadas, com as intenções definidas** no dataset.  
> A seguir, há um exemplo:  

![Exemplo de busca de intenção e resposta](https://docs.google.com/uc?export=download&id=1LnOTZiahBSv9VGrCSExbylNbxHpclMKZ)

> ## 5. Importação de bibliotecas
> Serão importados o pacote de expressões regulares do Python e o acesso ao WordNet dado pelo NLTK.
"""

import re
import nltk
nltk.download('omw-1.4') # Necessario download de omw-1.4 por erro na execucao
from nltk.corpus import wordnet
# Necessario download do wordnet
nltk.download('wordnet')
# Se usar Open Multilingual Wordnet
nltk.download('omw')

"""> ## 6. Construção da lista de palavras-chave
> <p align="justify">A etapa pode levar mais tempo, caso se pretenda definir as palavras manualmente. Cabe lembrar que, quanto mais palavras-chave houver, maior cobertura terá o chatbot.</p>
> <p align="justify">Para fins didáticos, a tentativa será automatizar a busca a partir de único termo, com uso de sinônimos encontrados no WordNet.</p>
"""

# Lista de palavras com a grafia usual
palavras=['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'horário', 'endereço','cardápio', 'pedido', 'delivery', 'reserva']
# Dicionarios de sinonimos
lista_sinonimos={}

# Percorre lista de palavras
for palavra in palavras:
  sinonimos=[]
  # Busca sinonimos da palavra no wordnet em pt-br
  for syn in wordnet.synsets(palavra, lang="por"):
    # Busca formas lexicas da palavra
    for lem in syn.lemmas(lang="por"):
      # Adiciona formas na lista
      sinonimos.append(lem.name())

  # Remove palavras duplicadas e adiciona ao dicionario
  lista_sinonimos[palavra]=set(sinonimos)

print(lista_sinonimos)

"""
> **OBSERVAÇÃO**: É possível adicionar mais palavras manualmente; remover sinônimo indesejado; adicionar frases completas ao invés de palavras-chave separadas."""

# Adiciona sinonimo inexistente no wordnet
lista_sinonimos['olá'].add('oi')
lista_sinonimos['olá'].add('bom dia')
lista_sinonimos['olá'].add('boa tarde')
lista_sinonimos['olá'].add('boa noite')
lista_sinonimos['olá'].add('tudo bem')
lista_sinonimos['olá'].add('como vai')
lista_sinonimos['endereço'].add('rua')
lista_sinonimos['endereço'].add('localização')
lista_sinonimos['endereço'].add('logradouro')
lista_sinonimos['endereço'].add('domicílio')
lista_sinonimos['endereço'].add('destino')
lista_sinonimos['endereço'].add('direção')
lista_sinonimos['cardápio'].add('pratos')
lista_sinonimos['delivery'].add('entregas')
lista_sinonimos['delivery'].add('entrega em domicílio')
lista_sinonimos['delivery'].add('entrega em casa')
lista_sinonimos['delivery'].add('leva-e-traz')
lista_sinonimos['delivery'].add('transportar')
lista_sinonimos['reserva'].add('agendamento')
lista_sinonimos['reserva'].add('marcar hora')
lista_sinonimos['reserva'].add('combinar hora')
lista_sinonimos['reserva'].add('reservação')
lista_sinonimos['pedido'].add('pedir comida')
lista_sinonimos['pedido'].add('comanda')
lista_sinonimos['pedido'].add('fazer pedido')
lista_sinonimos['pedido'].add('encomenda')

print(lista_sinonimos)

"""> ## 7. Construção do dicionário de intenções
> <p align="justify">Será utilizado o dicionário de sinônimos construído e mapeados os sinônimos para possíveis intenções. Além disso, as palavras-chave serão formatadas para que sejam interpretadas pela ferramenta de busca de expressões regulares.</p>
"""

# Dicionario de palavras-chave e intencoes
keywords={}
keywords_dict={}

# Cria novo registro de intencao para saudacoes
keywords['saudacao']=[]
# Popula a entrada criada com lista de sinonimos da palavra-chave "olá" e formata com metacaracteres do regex
for sin in list(lista_sinonimos['olá']):
  keywords['saudacao'].append('.*\\b'+sin+'\\b.*')

# Cria novo registro de intencao para horario de atendimento
keywords['horario_atendimento']=[]
# Popula a entrada criada com lista de sinonimos da palavra-chave "horário" e formata com metacaracteres do regex
for sin in list(lista_sinonimos['horário']):
  keywords['horario_atendimento'].append('.*\\b'+sin+'\\b.*')

# Cria novo registro de intencao para endereço
keywords['endereco']=[]
# Popula a entrada criada com lista de sinonimos da palavra-chave "endereço" e formata com metacaracteres do regex
for sin in list(lista_sinonimos['endereço']):
  keywords['endereco'].append('.*\\b'+sin+'\\b.*')

# Cria novo registro de intencao para cardapio
keywords['cardapio']=[]
# Popula a entrada criada com lista de sinonimos da palavra-chave "cardápio" e formata com metacaracteres do regex
for sin in list(lista_sinonimos['cardápio']):
  keywords['cardapio'].append('.*\\b'+sin+'\\b.*')

# Cria novo registro de intencao para pedido
keywords['pedido']=[]
# Popula a entrada criada com lista de sinonimos da palavra-chave "pedido" e formata com metacaracteres do regex
for sin in list(lista_sinonimos['pedido']):
  keywords['pedido'].append('.*\\b'+sin+'\\b.*')

# Cria novo registro de intencao para delivery
keywords['delivery']=[]
# Popula a entrada criada com lista de sinonimos da palavra-chave "delivery" e formata com metacaracteres do regex
for sin in list(lista_sinonimos['delivery']):
  keywords['delivery'].append('.*\\b'+sin+'\\b.*')

# Cria novo registro de intencao para reseva
keywords['reserva']=[]
# Popula a entrada criada com lista de sinonimos da palavra-chave "reserva" e formata com metacaracteres do regex
for sin in list(lista_sinonimos['reserva']):
  keywords['reserva'].append('.*\\b'+sin+'\\b.*')

for intent, keys in keywords.items():
  # Une todas palavras-chave sinonimas com o operador OU
  keywords_dict[intent]=re.compile('|'.join(keys))

print(keywords_dict)

""">**OBSERVAÇÕES:** Criou-se uma grande expressão regular, que pode achar todos os termos sinônimos para cada intenção.
><p align="justify">O `\b` utilizado na expressão regular define que será buscado o termo entre estes boundaries.</p>
><p align="justify">O `.*` define que o regex deve buscar o padrão em todo texto de entrada.</p>  
><p align="justify">Os sinais de `|` indicam o operador lógico OU para que qualquer um dos sinônimos ative o gatilho de busca.</p>

> ## 8. Definição das respostas
> Deve-se definir as respostas para cada intenção padrão, que será acionada quando não se encontra nenhuma palavra-chave na entrada do usuário.
"""

# Define o dicionário que associa as intenções as respostas - total de 8 intencoes apos melhoria
respostas={
    'saudacao':'Olá. Como posso ajudá-lo?',
    'horario_atendimento':'Nosso horário de funcionamento é a partir das 11h30 até 15h00.',
    'endereco':'Nosso endereço é Avenida Ronald do Brasil 1888, bairro Havaí.',
    'endereco':'Nosso endereço está no bairro Havaí, na Avenida Ronald do Brasil 1888.',
    'cardapio':'Veja nosso cardápio com pratos da culinária americana.',
    'cardapio':'Fique à vontade para escolher um prato do nosso cardápio.',
    'pedido':'Qual será o seu pedido?',
    'pedido':'Qual será a entrada do seu pedido?',
    'delivery':'O restaurante faz entregas na vizinhança localizada no raio de 15 km.',
    'delivery':'Nosso restaurante faz entregas na vizinhança dentro do raio de 15 km.',
    'reserva':'Recomendamos sempre fazer reserva para os finais de semana.',
    'reserva':'Para os finais de semana é recomendado sempre fazer reserva.',
    'padrao':'Me desculpe, mas não entendi o que você disse. Você poderia reformular?',
}

"""> **OBSERVAÇÃO**: Poderia ser criada mais de uma resposta para cada intenção e assim evitar a repetitividade na interação.

>## 9. Link das intenções e geração de repostas (front-end)
><p align="justify">Construção do algoritmo que fará a interação com o usuário (gerenciador de diálogo), onde recebe uma entrada do mesmo, e utilizando regex, há busca de palavras-chave no texto e associação com a intenção desejada.</p>
"""

print ("Bem-vindo ao restaurante McChat. ")

# Roda indefinidamente ate usuario pedir para sair
while (True):

    # Pega input do usuario e normaliza em letras minusculas
    entrada = input().lower()

    # Define condicao de saida
    if entrada == 'sair':
        print ("Obrigado pela visita.")
        break

    matched_intent = None

    for intent,pattern in keywords_dict.items():

      # Busca palavras-chave na entrada do usuario com regex
      if re.search(pattern, entrada):

        # Se encontra, guarda o nome da intencao correspondente
        matched_intent=intent

    # Por padrao, define-se intencao padrao
    key='padrao'
    if matched_intent in respostas:
      key = matched_intent

    # Chatbot imprime a resposta correspondente
    print (respostas[key])

    # LEMBRETE DE INTENCOES PARA TESTE:['boa noite','horário','endereço','cardápio','pedido','delivery','reserva']

""">## 10. O que fazer para melhorar o projeto?
>A abordagem e a arquitetura de chatbot são mais simplificadas, dependentes do tamanho e cobertura da base de dados para funcionar. Para posterior melhoria do projeto, recomendam-se estas opções:</p>
>*  Incluir mais intenções na base de dados relacionadas a um restaurante (endereço, cardápio, delivery, reservas) - OK!
>*  Criar regra específica para reserva de mesas no restaurante em que as reservas são salvas em dicionário e, com uso de regex, para obter parâmetros de data, horário e quantidade de pessoas no meio do texto.   
>*  Resolver a intenção de horário de atendimento para possibilidade de restaurante abrir no almoço e jantar.

> ## 11. Referências e material complementar
>* [Criando meu ChatBot com Python](https://medium.com/@erikatiliorey/criando-um-chatbot-com-python-36f24b62df6c)
>* [Introducing Conversational Chat bots using Rule Based Approach](https://chatbotslife.com/introducing-conversational-chat-bots-using-rule-based-approach-c8840aeaad07)
>* [Building a Simple Chatbot from Scratch in Python (using NLTK)](https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e)
>* [How to write a smart Chatbot in 40 lines without ML](https://levelup.gitconnected.com/a-chatbot-without-machine-learning-b76ad00e30c1)
>* [Building a Rule-based Chatbot in Python](https://blog.datasciencedojo.com/building-a-rule-based-chatbot-in-python/)
>* [Basic FAQ chat bot](https://github.com/canonicalmg/FAQ-Chat-Bot)
>* Notebook elaborado a partir de projeto desenvolvido pelo Prof. [Lucas Oliveira](http://lattes.cnpq.br/3611246009892500).
"""
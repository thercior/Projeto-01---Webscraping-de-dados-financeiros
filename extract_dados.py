#======================= PROGRAMA PARA EXTRAÇÃO WEB DE DADOS FINANCEIROS =====================#

#Importação das bibliotecas
import requests
import locale
from bs4 import BeautifulSoup
from tabulate import tabulate
from modelos import FundosImobiliario, Estrategia

#============================================================================#
#biblioteca para fazer conversão das variáveis de um sistema para outro
locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')

#Funções para tratar os respectivos dados
def trata_porcentagem(porcentagem_str):
    #7,05%
    return locale.atof(porcentagem_str.split('%')[0])

def trata_decimal(decimal_str):
    # R$ 5.000,84
    return locale.atof(decimal_str)

#============================================================================#
#Definição da url de chamada e o agente que está requisitando
url = 'https://www.fundamentus.com.br/fii_resultado.php'
headers = {'User-Agent':'Mozilla/5.0'}
try:
    #Executação da chamada: Pode ser GET, POST, PUT... depende da que o site utiliza.
    resposta = requests.post(url, headers=headers)

    # Execução da BeautifulSoup para poder fazer o parsing da variável resposta
    # Isto é necessário para poder transformar a variável para um dicionário (mais legível)
    soup = BeautifulSoup(resposta.text,'html.parser')

    # Retorno dos resultados de acordo com o que se deseja procurar 
    tabela = soup.find(id='tabelaResultado')
    linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

    #============================================================================#

    # Montagem de lista filtrada de dados financeiros de acordo com critérios estabelecidos
    resultado = []

    # Critérios para filtrar os dados financeiros
    estrategia = Estrategia(
        cotacao_atual_min=10,
        dividiend_yield_min=5,
        p_vp_min=0.8,
        valor_mercado_min=200000,
        liquidez_min=500,
        qt_min_imoveis=5,
        max_vacancia_media=10
    )

    # Obtenção dos dados de acordo com os critérios
    for linha in linhas:
        dados_fundo = linha.find_all('td')
        codigo = dados_fundo[0].text
        segmento = dados_fundo[1].text
        cotacao = trata_decimal(dados_fundo[2].text)
        ffo_yield = trata_porcentagem(dados_fundo[3].text)
        dividiend_yield = trata_porcentagem(dados_fundo[4].text)
        p_vp = trata_decimal(dados_fundo[5].text)
        valor_mercado = trata_decimal(dados_fundo[6].text)
        liquidez = trata_decimal(dados_fundo[7].text)
        qt_imoveis = int(dados_fundo[8].text)
        preco_m2 = trata_decimal(dados_fundo[9].text)
        aluguel_m2 = trata_decimal(dados_fundo[10].text)
        cap_rate = trata_porcentagem(dados_fundo[11].text)
        vacancia = trata_porcentagem(dados_fundo[12].text)
        
        fundo_imobiliario = FundosImobiliario(codigo, segmento, cotacao, ffo_yield,dividiend_yield,
                    p_vp, valor_mercado, liquidez, qt_imoveis, preco_m2, aluguel_m2,
                    cap_rate, vacancia)
        
        # verifica os critérios estabelecidos de acordo com a estratégia
        if estrategia.aplica_estrategia(fundo_imobiliario):
            resultado.append(fundo_imobiliario) # retorna os dados filtrados para a lista criada

    #Saída de dados em forma de tabela no terminal por meio da biblioteca tabulate

    cabecalho = ["Código", "Segmento", "Cotação Atual", "Dividend Yield"]

    tabela = [] # lista para pegar os dados extraidos e filtrados de acordo com os parâmetros definidos no cabeçalho

    for elemento in resultado:
        tabela.append([
            elemento.codigo,
            elemento.segmento,
            locale.currency(elemento.cotacao_atual),
            f'{locale.str(elemento.dividiend_yield)}%'
            ])

    print(tabulate(tabela, headers=cabecalho, showindex='always', tablefmt='fancy_grid'))
except Exception:
    print(Exception)
    
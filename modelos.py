# =========== Definição do objeto Fundo imobiliário =================================
class FundosImobiliario:
    def __init__(self,codigo, segmento, cotacao_atual, ffo_yield,dividiend_yield,
                 p_vp, valor_mercado, liquidez, qt_imoveis, preco_m2, aluguel_m2,
                 cap_rate, vacancia_media):
        self.codigo = codigo
        self.segmento = segmento
        self.cotacao_atual = cotacao_atual
        self.ffo_yield = ffo_yield
        self.dividiend_yield = dividiend_yield
        self.p_vp = p_vp
        self.valor_mercado = valor_mercado
        self.liquidez = liquidez
        self.qt_imoveis = qt_imoveis
        self.preco_m2 = preco_m2
        self.aluguel_m2 = aluguel_m2
        self.cap_rate = cap_rate
        self.vacancia_media = vacancia_media

#================== Definição das estratégias: critérios avaliados e filtragem de dados ================
class Estrategia:
   
    def __init__(self, segmento="", cotacao_atual_min=0, ffo_yield_min=0,dividiend_yield_min=0,
                 p_vp_min=0, valor_mercado_min=0, liquidez_min=0, qt_min_imoveis=0, valor_min_preco_m2=0, 
                 valor_min_aluguel_m2=0, valor_min_cap_rate=0, max_vacancia_media=0):
        self.segmento = segmento
        self.cotacao_atual_min = cotacao_atual_min
        self.ffo_yield_min = ffo_yield_min
        self.dividiend_yield_min = dividiend_yield_min
        self.p_vp_min = p_vp_min
        self.valor_mercado_min = valor_mercado_min
        self.liquidez_min = liquidez_min
        self.qt_min_imoveis = qt_min_imoveis
        self.valor_min_preco_m2 = valor_min_preco_m2
        self.valor_min_aluguel_m2 = valor_min_aluguel_m2
        self.valor_min_cap_rate = valor_min_cap_rate
        self.max_vacancia_media = max_vacancia_media
    
    def aplica_estrategia(self, fundo: FundosImobiliario):   
        if self.segmento != "" and fundo.segmento != self.segmento:
            return False
                        
        #Filtragem para condições especificadas
        if fundo.cotacao_atual < self.cotacao_atual_min \
            or fundo.ffo_yield < self.ffo_yield_min \
            or fundo.dividiend_yield < self.dividiend_yield_min \
            or fundo.p_vp < self.p_vp_min \
            or fundo.valor_mercado < self.valor_mercado_min \
            or fundo.liquidez < self.liquidez_min \
            or fundo.qt_imoveis < self.qt_min_imoveis \
            or fundo.preco_m2 < self.valor_min_preco_m2 \
            or fundo.aluguel_m2 < self.valor_min_aluguel_m2 \
            or fundo.cap_rate < self.valor_min_cap_rate \
            or fundo.vacancia_media > self.max_vacancia_media:
            return False
        else:
            return True


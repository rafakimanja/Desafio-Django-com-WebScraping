import re

class Refatora:

    @staticmethod
    def extrair_valores(texto):
        padroes = {
            'Objeto': r'Objeto:\s*(.*?)(?=\s*Órgão|$)',
            'Modalidade de Contratação': r'Modalidade da Contratação:\s*(.*?)(?=\s*Órgão:|$)',
            'Órgão': r'Órgão:\s*(.*?)(?=\s*Local|$)',
            'Local': r'Local:\s*(.*?)(?=\s*Objeto|$)'
        }
        valores = {}
        for campo, padrao in padroes.items():
            valor = re.search(padrao, texto)
            if valor:
                valores[campo] = valor.group(1).strip()
        return valores

    @staticmethod
    def modifica_modalidade(dicionario):
        if 'Ú' in dicionario['Modalidade de Contratação']:
            texto = dicionario['Modalidade de Contratação']
            texto_refatorado = texto[:texto.find('Ú')].strip()
            return texto_refatorado

    @staticmethod
    def refatora_dinheiro(lista):
        for i, item in enumerate(lista):
            if 'R$' in item:
                lista[i] = item.replace('\xa0', '')

        return lista

    @staticmethod
    def extrair_valores_itens(lista, objedo_bd):
        lista_itens = []
        controle = 0
        for i, item in enumerate(lista):
            dados_itens = {}
            match controle:
                case 0:
                    dados_itens['numero'] = item
                    controle += 1
                case 1:
                    dados_itens['descricao'] = item
                    controle += 1
                case 2:
                    dados_itens['quantidade'] = item
                    controle += 1
                case 3:
                    dados_itens['valor_unitario'] = item
                    controle += 1
                case 4:
                    dados_itens['valor'] = item
                    controle = 0

            lista_itens.append(dados_itens.copy())

        return lista_itens
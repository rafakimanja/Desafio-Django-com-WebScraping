from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from scraping.refatora_string import Refatora
from scraping.models import Licitacao, Itens


def roda_script(request):

    if request.method == 'GET':
    
        ref = Refatora()
        database = []

        #configurações do selenium
        url = 'https://pncp.gov.br/app/editais?q=&status=recebendo_proposta&pagina=1'
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(options=option)
        driver.get(url)

        sleep(3)

        #pega os dados dos editais
        html_content = driver.page_source
        site = BeautifulSoup(html_content, "html.parser")
        links = site.find_all('a', class_='br-item')

        #adicionando os dados dos editais e convertendo para dicionario
        editais = links[0:10]

        #checando a quantidade de paginação
        paginacao = driver.find_element(By.XPATH, '//*[@id="main-content"]/pncp-list/pncp-results-panel/pncp-tab-set/div/pncp-tab[1]/div/div[2]/div[2]/div[3]/pncp-pagination/nav/ul/li[10]/button')
        num_paginas = paginacao.text

        sleep(2)

        for j in range(0, int(num_paginas)): #loop de acordo com a quantidade de páginas

            for c in range(1, 11): #loop para os 10 itens de licitações da página

                list_itens = []
                licitacoes = []
                bd_itens = []

                valores = ref.extrair_valores(editais[c-1].get_text())

                valores["Modalidade de Contratação"] = ref.modifica_modalidade(valores)

                licitacoes.append(valores.copy())
                valores.clear()

                #sando no banco de dados
                nova_licitacao = Licitacao(descricao=valores['Objeto'], modalidade=valores['Modalidade de Contratação'], comprador=(valores['Órgão']+' | '+valores['Local']))
                nova_licitacao.save()

                sleep(2)

                # abre a licitação
                xpath_lic = f'//*[@id="main-content"]/pncp-list/pncp-results-panel/pncp-tab-set/div/pncp-tab[1]/div/div[2]/div[2]/div[2]/pncp-items-list/div/div[{c}]/a'
                licitacao = driver.find_element(By.XPATH, xpath_lic)
                driver.execute_script('arguments[0].click();', licitacao)

                sleep(10)

                #qtd de itens da licitação
                qtd_itens = driver.find_element(By.XPATH,'//*[@id="main-content"]/pncp-item-detail/div/pncp-tab-set/div/pncp-tab[1]/div/div/pncp-table/div/ngx-datatable/div/datatable-footer/div/pncp-pagination-table/div/div[3]')
                itens_atual = qtd_itens.text[2]
                itens_total = qtd_itens.text[7]

                if itens_atual != itens_total:

                    while itens_atual != itens_total:
                        sleep(1.5)
                        qtd_itens = driver.find_element(By.XPATH, '//*[@id="main-content"]/pncp-item-detail/div/pncp-tab-set/div/pncp-tab[1]/div/div/pncp-table/div/ngx-datatable/div/datatable-footer/div/pncp-pagination-table/div/div[3]')
                        itens_atual = qtd_itens.text[2]
                        itens_total = qtd_itens.text[7]

                        # colheta o HTML dos Itens
                        html_content = driver.page_source
                        licitacao_content = BeautifulSoup(html_content, "html.parser")
                        itens = licitacao_content.find_all('span', class_='ng-star-inserted')
                        itens = itens[11:]

                        # pega os dados dos itens
                        for item in itens:
                            if item.get_text() == 'Nome':
                                break
                            else:
                                list_itens.append(item.get_text())

                        # reformata os valores de dinheiro
                        list_itens = ref.refatora_dinheiro(list_itens)

                        # formatando os dados em um dicionario e atribui os dados em uma lista
                        #bd_itens.append(ref.extrair_valores_itens(list_itens))
                        
                        
                        controle = 0
                        for i, item in enumerate(list_itens):
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
                            
                            
                            novo_item = Itens(descricao=dados_itens['descricao'], unidade='', quantidade=dados_itens['quantidade'], valor=dados_itens['valor'], licitacao=nova_licitacao)
                            novo_item.save()

                        #altera a pagina dos itens
                        muda_itens = driver.find_element(By.XPATH, '//*[@id="btn-next-page"]/i')
                        driver.execute_script('arguments[0].click();', muda_itens)

                else:

                    #colheta o HTML dos Itens
                    html_content = driver.page_source
                    licitacao_content = BeautifulSoup(html_content, "html.parser")
                    itens = licitacao_content.find_all('span', class_='ng-star-inserted')
                    itens = itens[11:]

                    #pega os dados dos itens
                    for item in itens:
                        if item.get_text() == 'Nome':
                            break
                        else:
                            list_itens.append(item.get_text())

                    #reformata os valores de dinheiro
                    list_itens = ref.refatora_dinheiro(list_itens)

                    #formatando os dados em um dicionario e atribui os dados em uma lista
                    bd_itens.append(ref.extrair_valores_itens(list_itens))

                # atribuindo os dados ao database
                database.append(licitacoes[:])
                database.append(bd_itens[:])

                driver.back()

            troca_pagina = driver.find_element(By.XPATH,'//*[@id="main-content"]/pncp-list/pncp-results-panel/pncp-tab-set/div/pncp-tab[1]/div/div[2]/div[2]/div[3]/pncp-pagination/nav/ul/li[11]/button/i')
            driver.execute_script('arguments[0].click();', troca_pagina)
            sleep(2)

        for i, objeto in enumerate(database):
            if i%2 == 0:
                print(f'{i}°In. | Licitação: {objeto}')
            else:
                print(f'{i}°In. | Itens pedido: {objeto}')

            return render(request, 'index.html')

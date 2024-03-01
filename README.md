# Desafio Django com WebScraping
 
Este é um projeto proposto como desafio de Web Scraping de uma página web a partir de um servidor Django.
Para a execução do desafio escolhi implementar uma versão que capta dados da seguinte URL: https://pncp.gov.br/app/editais?q=&&status=recebendo_proposta&pagina=1

 ### Motivo

Decidi escolher este pois foi o site que senti maior facilidade em implementar a solução, visto que, nunca tinha realizado nenhuma tarefa envolvendo Web Scraping ou automação, 
o site apresentava uma interface mais amigável para a realizar a automação


### Tecnologias

Para realizar as tarefas propostas no desafio utilizei:
- Selenium -> para controle do navegador
- BeautifulSoup -> para fazer a raspagem dos dados
- Django + SQLite3 -> para rodar o programa e persistencia dos dados como foi solicitado


### Utilização

Não foi criada nenhuma restrição para a utilização do programa, basta clonar o repositório para a sua máquina e rodar através do do comando padrão do Django 'python.exe manage.py runserver'
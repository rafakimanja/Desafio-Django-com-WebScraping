from django.db import models

class Licitacao(models.Model):
    descricao = models.CharField(max_length=255)
    modalidade = models.CharField(max_length=100)
    comprador = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao


class Itens(models.Model):
    descricao = models.CharField(max_length=255)
    unidade = models.CharField(max_length=50)
    quantidade = models.IntegerField()
    valor = models.CharField(max_length=50)
    licitacao = models.ForeignKey(to=Licitacao, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao



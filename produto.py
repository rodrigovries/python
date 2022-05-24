#representa uma entidade no banco de dados

class Produto:

    def __init__(self, descricao, preco, quantidade, id):
        self.id = id
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

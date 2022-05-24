# dao.py
import sqlite3

from produto import Produto

SQL_PREPARA_BANCO = 'create table if not exists produto ' \
                    '(descricao varchar(60) not null,' \
                    'preco double not null, ' \
                    'quantidade integer not null)'

SQL_SALVA_PRODUTO = 'insert into produto values (?, ?, ?);'
SQL_LISTA_PRODUTOS = 'select descricao, preco, quantidade, rowid from produto;'
SQL_DELETA_PRODUTO = 'delete FROM produto WHERE rowid=?;'
SQL_BUSCA_POR_ID = 'select descricao, preco, quantidade, rowid from produto where rowid=?;'
SQL_ATUALIZA_PRODUTO = 'update produto SET descricao=?, preco=?, quantidade=? where rowid=?;'

# crud - > create, read, update, delete
class ProdutoDao:
    def __init__(self, nome_banco):
        self.__nome_banco = nome_banco
        self.prepara_banco()

    def prepara_banco(self):
        conexao = sqlite3.connect(self.__nome_banco)
        conexao.cursor().execute(SQL_PREPARA_BANCO)
        conexao.commit() # comita (confirma), senao nao tem efeito

    def salvar(self, produto):
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()

        if (produto.id != None) and len(produto.id) > 0:
            cursor.execute(SQL_ATUALIZA_PRODUTO, (produto.descricao, produto.preco, produto.quantidade, produto.id))
        else:
            cursor.execute(SQL_SALVA_PRODUTO, (produto.descricao, produto.preco, produto.quantidade))
            produto.id = cursor.lastrowid

        conexao.commit()
        return produto

    def listar(self):
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_LISTA_PRODUTOS)
        produtos = traduz_produtos(cursor.fetchall())
        return produtos

    def deletar(self, id):
        conexao = sqlite3.connect(self.__nome_banco)
        conexao.cursor().execute(SQL_DELETA_PRODUTO, [id])
        conexao.commit()

    def buscar_por_id(self, id):
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_BUSCA_POR_ID, [id])
        tupla = cursor.fetchone() #('descricao', 1999, 10, 1)
        return Produto(tupla[0], tupla[1], tupla[2], tupla[3])

def traduz_produtos(produtos):
    def cria_produto_com_tupla(tupla):
        return Produto(tupla[0], tupla[1], tupla[2], tupla[3])
    return list(map(cria_produto_com_tupla, produtos))

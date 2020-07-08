from flask import Flask, request
import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="lojas"
)

# Parte que transforma o retorno do banco de dados em json
def toJson(registos):
    lista = []
    for ID, nome, preco, quantidade in registos:
        helper = '{"id": %d,"nome":"%s","preco": %d, "quantidade":%d}' % (ID, nome, preco, quantidade)
        result = json.loads(helper)
        lista.append(result)
    return json.dumps(lista)
mycursor = mydb.cursor()

app= Flask(__name__)

@app.route("/", methods=["POST"])
def listar_lojas():
    body = request.get_json()
    mycursor.execute("SELECT * FROM produtos")
    result = mycursor.fetchall()
    return toJson(result)



# Criador de lojas
@app.route("/adicionar/loja", methods=["POST"])
def adicionar_loja():
    body = request.get_json()
    nome_loja = body["nome_loja"]
    senha_loja = body["senha_loja"]
    gerente_loja = body["gerente_loja"]
    id_gerente = body["id_gerente"]

    try:
        mycursor.execute("INSERT INTO lojas_cadastradas(nome_loja, gerente_loja, senha_loja, id_gerente) VALUES ('%s', '%s', '%s', '%d')" % (nome_loja, gerente_loja, senha_loja, id_gerente))
        mydb.commit()
        mydb.cursor()
        mycursor.execute("SELECT id_loja FROM lojas_cadastradas")
        Identity = mycursor.fetchall()
        f = 0
        for i in Identity:
            f = i
        mydb.cursor()
        sql = "CREATE TABLE %s(id int, nome VARCHAR(30), preco int(10), quantidade int(10), PRIMARY KEY(id));" % ("loja"+str(f[0]))
        mycursor.execute(sql)
        return {"status":"sucess", "loja_id":f[0]}
    except:
        return {"message":"Falha ao inserir a Loja"}


#  Criador de Produtos
@app.route("/adicionar/produto", methods=["POST"])
def adicionar_produto():
    body = request.get_json()
    id_loja = body["id_loja"]
    senha_loja = body["senha_loja"]
    nome_produto = body["nome_produto"]
    quantidade = body["quantidade"]
    preco = body["preco"]

    try:
        mydb.cursor()
        mycursor.execute("SELECT id_loja, senha_loja FROM lojas_cadastradas")
        db_data = mycursor.fetchall()
        for a, b in db_data:
            if id_loja == a and senha_loja == b:
                mydb.cursor()
                sql = "INSERT INTO %s(nome, quantidade, preco) VALUES ('%s', %d, %d)" % ("loja"+str(a),nome_produto, quantidade, preco)
                mycursor.execute(sql)
                mydb.commit()
                return {"message":"Produto inserido com sucesso"}
        return {"message":"O produto nao foi encontrado"}
    except:
        return {"message":"Falha ao inserir o produto"}

#Eliminador de lojas
@app.route("/eliminar/loja", methods=["POST"])
def eliminar_loja():
    body = request.get_json()
    id_loja = body["id_loja"]
    senha_loja = body["senha_loja"]
    gerente_loja = body["gerente_loja"]
    id_gerente = body["id_gerente"]
    try:
        mydb.cursor()
        mycursor.execute("SELECT id_loja, senha_loja, gerente_loja, id_gerente FROM lojas_cadastradas")
        db_data = mycursor.fetchall()
        for a, b, c, d in db_data:
            if a == id_loja and b == senha_loja and c == gerente_loja and d == id_gerente:
                mydb.cursor()
                mycursor.execute("DELETE FROM lojas_cadastradas WHERE id_loja=%d" % a)
                mydb.commit()
                mydb.cursor()
                mycursor.execute("DROP TABLE %s" % ("loja"+str(a)))
                return {"message":"Loja eliminada com sucesso"}
        return {"message":"Loja nao encontrada"}
    except:
        return {"message":"Falha ao Eliminar a loja"}

@app.route("/atualizar", methods=["POST"])
def atualizarUsuario():
    body = request.get_json()
    try:
        mycursor.execute("UPDATE produtos SET preco=%d, quantidade=%d WHERE id=%d" % (body["preco"], body["quantidade"], body["id"]))
        mydb.commit()
        return {"message":"Usuario atualizado com sucesso"}
    except:
        return {"message":"Falha ao atualizar os dados"}

@app.route("/filtrar", methods=["POST"])
def filtrarUsuario():
    body = request.get_json()
    try:
        mycursor.execute("SELECT * FROM produtos WHERE nome LIKE '%"+body["texto"]+"%'")
        result = mycursor.fetchall()
        return toJson(result)
    except:
        return {"message":"Falha ao connectar ao servidor"}

if __name__ == '__main__':
	app.run()


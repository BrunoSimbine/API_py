from flask import Flask, request
import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="primeiro"
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

try:
    mycursor.execute("CREATE TABLE produtos (id INTEGER PRIMARY KEY, nome VARCHAR(30), preco INTEGER(10), quantidade INTEGER(10))")
except:
    print("Tabela ja criada")


app= Flask(__name__)

@app.route("/")
def home():
    mycursor.execute("SELECT * FROM produtos")
    result = mycursor.fetchall()
    return toJson(result)


@app.route("/cadastrar", methods=["POST"])
def cadastrarUsuario():
    body = request.get_json()
    nome = body["nome"]
    preco = body["preco"]
    quantidade = body["quantidade"]
    try:
        mycursor.execute("INSERT INTO produtos(nome, preco, quantidade) VALUES ('%s', %d, %d)" % (nome, preco, quantidade))
        mydb.commit()
        return {"message":"Cadastro efectuado com sucesso"}
    except:
        return {"message":"Falha ao registar no banco de dados"}


@app.route("/atualizar", methods=["POST"])
def atualizarUsuario():
    body = request.get_json()
    try:
        mycursor.execute("UPDATE produtos SET preco=%d, quantidade=%d WHERE id=%d" % (body["preco"], body["quantidade"], body["id"]))
        mydb.commit()
        return {"message":"Usuario atualizado com sucesso"}
    except:
        return {"message":"Falha ao atualizar os dados"}

@app.route("/apagar", methods=["POST"])
def apagarUsuario():
    body = request.get_json()
    try:
        mycursor.execute("DELETE FROM produtos WHERE id= %d" % body["id"])
        mydb.commit()
        return {"message":"Usuario removido com sucesso"}
    except:
        return {"message":"Falha ao eliminar o usuario"}


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


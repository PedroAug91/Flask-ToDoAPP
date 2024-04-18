from flask import Flask
from flask import render_template, redirect, url_for, session, request
import mysql.connector

app = Flask(__name__)
app.secret_key = "admin"

def connect_to_database():
    conexao = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="admin",
        database="FlaskToDo"
    )

    return conexao

@app.route("/", methods=["GET", "POST"])
def home():
    if ("nome" not in session):
        return redirect(url_for("login"))

    if (request.method == "POST"):
        conexao = connect_to_database()
        cursor = conexao.cursor(dictionary=True)

        valores = (session["id_usuario"], )

        sql = "SELECT ativo, descricao FROM tarefa WHERE id_usuario = %s AND ativo = 1"
        tarefas_ativas = cursor.execute(sql, valores)
        
        sql = "SELECT ativo, descricao FROM tarefa WHERE id_usuario = %s AND ativo = 0"
        tarefas_inativas = cursor(sql, valores)

        cursor.close()
        conexao.close()

    
        return render_template("home.html", title="Tarefas", active_tasks=tarefas_ativas, inactive_tasks=tarefas_inativas)

    return render_template("home.html", title="Tarefas", active_tasks=None, inactive_tasks=None)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if (request.method == "POST"):
        nome = request.form["username"]
        email = request.form["email"]
        senha = request.form["password"]

        conexao = connect_to_database()
        cursor = conexao.cursor(dictionary=True)

        sql ="SELECT * FROM usuario WHERE email = %s"
        valores = (email, )
        cursor.execute(sql, valores) 
        usuario = cursor.fetchone()
        
        if (usuario is not None):
            error = "Este email já foi cadastrado, tente outro."
        else:
            sql = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)"
            valores = (nome, email, senha)


            cursor.execute(sql, valores)
            conexao.commit()
            
            sql = "SELECT id_usuario FROM usuario WHERE email = %s"
            valores = (email, )
            cursor.execute(sql, valores)

            id_usuario = cursor.fetchone()

            cursor.close()
            conexao.close()

            session["nome"] = nome
            session["id_usuario"] = id_usuario["id_usuario"]
            return redirect(url_for("home"))

    return render_template("signup.html", title="Cadastrar", error=error)


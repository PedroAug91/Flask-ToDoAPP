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

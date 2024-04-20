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

    tarefas_inativas = tarefas_ativas = None

    conexao = connect_to_database()
    cursor = conexao.cursor(dictionary=True)

    valores = (session["id_usuario"], )

    sql = "SELECT id_tarefa, descricao FROM tarefa WHERE id_usuario = %s AND ativo = 1"
    cursor.execute(sql, valores)
    tarefas_ativas = cursor.fetchall()
    
    sql = "SELECT id_tarefa, descricao FROM tarefa WHERE id_usuario = %s AND ativo = 0"
    cursor.execute(sql, valores)
    tarefas_inativas = cursor.fetchall()

    cursor.close()
    conexao.close()

    if (tarefas_ativas == None and tarefas_inativas is None):
        return render_template("home.html", title="Tarefas", active_tasks=None, inactive_tasks=None)
    elif (tarefas_ativas == None and tarefas_inativas != None):
        return render_template("home.html", title="Tarefas", active_tasks=None, inactive_tasks=tarefas_inativas)
    elif (tarefas_ativas != None and tarefas_inativas == None):
        return render_template("home.html", title="Tarefas", active_tasks=tarefas_ativas, inactive_tasks=None)
    
    return render_template("home.html", title="Tarefas", active_tasks=tarefas_ativas, inactive_tasks=tarefas_inativas)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if ("nome" in session):
        return redirect(url_for("home"))

    error = None

    if (request.method == "POST"):
        email = request.form["email"]
        senha = request.form["password"]

        conexao = connect_to_database()
        cursor = conexao.cursor(dictionary=True)

        sql = "SELECT id_usuario, nome, email, senha FROM usuario WHERE email = %s"
        valores = (email, )
        cursor.execute(sql, valores)
        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if (usuario is None):
            error = "Essa conta não existe."
        elif (usuario["senha"] != senha):
            error = "Senha incorreta, tente novamente."
        else:
            session["nome"] = usuario["nome"]
            session["id_usuario"] = usuario["id_usuario"]

            return redirect(url_for("home"))
    
    return render_template("login.html", title="Entrar", error=error)

@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))

@app.route("/create", methods=["GET","POST"])
def create():
    if ("nome" not in session):
        return redirect(url_for("/login"))

    if (request.method == "POST"):
        descricao = request.form["description"]

        conexao = connect_to_database()
        cursor = conexao.cursor(dictionary=True)
        
        sql = "INSERT INTO tarefa (descricao, id_usuario) VALUES (%s, %s)"
        valores = (descricao, session["id_usuario"])

        cursor.execute(sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect(url_for("home"))

    return render_template("create.html", title="Criar")

@app.route("/complete/<int:id_tarefa>", methods=["POST"])
def complete(id_tarefa):
    conexao = connect_to_database()
    cursor = conexao.cursor(dictionary=True)
    
    sql = "UPDATE tarefa SET ativo = 0 WHERE id_tarefa = %s"
    valores = (id_tarefa, )

    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
    return redirect(url_for("home"))

@app.route("/alter/<int:id_tarefa>", methods=["POST"])
def alter(id_tarefa):
    conexao = connect_to_database()
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT ativo FROM tarefa WHERE id_tarefa = %s"
    valores = (id_tarefa, )

    cursor.execute(sql, valores)
    tarefa = cursor.fetchone() 

    if(tarefa["ativo"] == 1):
        sql = "UPDATE tarefa SET ativo = 0 WHERE id_tarefa = %s"
    else:
        sql = "UPDATE tarefa SET ativo = 1 WHERE id_tarefa = %s"

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(url_for("home"))

@app.route("/remove/<int:id_tarefa>", methods=["POST"])
def remove(id_tarefa):
    conexao = connect_to_database()
    cursor = conexao.cursor(dictionary=True)

    sql = "DELETE FROM tarefa WHERE id_tarefa = %s"
    valores = (id_tarefa, )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()
    
    return redirect(url_for("home"))

# if (__name__ == "__main__"):
#     app.run(debug=True)
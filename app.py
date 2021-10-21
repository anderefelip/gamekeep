from flask import *
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret"

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    msg = "msg"
    if request.method == "POST":
        if (request.form["username"]!= "" and request.form["password"]!= ""):
            username = request.form["username"]
            password = request.form["password"]
            con = sqlite3.connect("dbjogos.db")
            c = con.cursor()
            c.execute("INSERT INTO login_users (username, password) VALUES (?,?)",(username,password))
            con.commit()
            msg = "Sua conta foi criada!"
            con.close()
            return redirect(url_for("login"))
        else:
            msg = "Conta não foi criada, tente novamente"
    return render_template("signup.html", msg = msg)

@app.route("/login", methods = ["GET", "POST"])
def login():
    msg = "msg"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        con = sqlite3.connect("dbjogos.db")
        c = con.cursor()
        c.execute("SELECT * FROM login_users WHERE username = '"+username+"' and password = '"+password+"'")
        res = c.fetchall()
        
        if len(res) ==1:
            return redirect(url_for("index"))
        else:
            msg = "Verifique seu login e senha!"
    return render_template("login.html", msg = msg)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("start"))

@app.route("/addgame")
def add():
   return render_template("addgame.html")

@app.route("/savegame",methods = ["POST","GET"])
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":
        try:  
            nome = request.form["nome"]   
            genero = request.form["genero"]  
            datainicio = request.form["datainicio"]  
            
            with sqlite3.connect("dbjogos.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into jogosdb (nome, genero, datainicio) VALUES (?,?,?)",(nome,genero,datainicio))   
                con.commit()  
                msg = "Jogo adicionado a sua biblioteca"
        except:
            msg = "Não foi possivel adicionar o jogo"
        finally:   
            return render_template("complete.html",msg = msg)
            con.close()

@app.route("/gameslibrary")  
def view():
    con = sqlite3.connect("dbjogos.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM jogosdb")
    rows = cur.fetchall()
    return render_template("gameslibrary.html",rows = rows)

@app.route("/deletegame")
def delete():
    return render_template("deletegame.html")

@app.route("/deletinho",methods = ["POST"])
def deletinho():
    id = request.form["id"]
    with sqlite3.connect("dbjogos.db") as con:
        try:
            cur = con.cursor()  
            cur.execute("DELETE FROM jogosdb WHERE id = ?",id)
            msg = "Jogo excluido da biblioteca!!"
        except:
            msg = "Não pode ser excluido"
        finally:
            return render_template("deletinho.html",msg = msg)

if __name__ == '__main__':
   app.run(debug = True)
from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
   return render_template("index.html")

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
                cur.execute("INSERT into jogosdb (nome, genero, datainicio) values (?,?,?)",(nome,genero,datainicio))   
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

if __name__ == '__main__':
   app.run(debug = True)
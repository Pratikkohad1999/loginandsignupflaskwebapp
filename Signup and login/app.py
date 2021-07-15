from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "hello"


@app.route("/", methods = ["GET", "POST"])
def home():
    msg = None
    if(request.method == "POST"):
        if(request.form["username"]!= "" and request.form["password"] ):
            username = request.form["username"]
            password = request.form["password"]
            conn = sqlite3.connect("signup.db")
            c = conn.cursor()
            c.execute("INSERT INTO person VALUES('"+username+"','"+password+"')")
            msg = "Your account is created !!!"
            conn.commit()
            conn.close()
        else: 
            msg = "Something wents wrong"

    return render_template("signup.html", msg = msg)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    r = ""
    msg = ""
    if(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("signup.db")
        c = conn.cursor()
        c.execute("SELECT * FROM person WHERE username = '"+username+"' and password = '"+password+"'")
        r = c.fetchall()
        for i in r:
            if(username == i[0] and password == i [1]):
                session["logedin"] = True
                session["username"] = username
                return redirect (url_for("about"))
            else:
                msg = "Please enter valid credentials"
    return render_template("login.html", msg = msg)
    
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug = True)


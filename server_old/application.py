from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import datetime
import time
import random

uname = ""
dpass1 = ""
alerttext = ""
color = ""

app = Flask(__name__)

dbusers = sqlite3.connect("users.db")
cu = dbusers.cursor()
dbnotes = sqlite3.connect("notes.db")
cn = dbnotes.cursor()

try:
    cu.execute(
        "CREATE TABLE users(id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, email TEXT, phone TEXT, uname TEXT, pass TEXT, sques TEXT, ans TEXT)")
except:
    pass


def insertNewAcc(fname, lname, email, phone, uname, password, sques, ans):
    dbusers = sqlite3.connect("users.db")
    cu = dbusers.cursor()
    cu.execute(
        "INSERT INTO users(firstname, lastname, email, phone, uname, pass, sques, ans) VALUES (?, ?, ?, ?, ?, ?, ? ,?)",
        (fname, lname, email, phone, uname, password, sques, ans))
    dbusers.commit()


def createTable(uname):
    dbnotes = sqlite3.connect("notes.db")
    cn = dbnotes.cursor()
    cn.execute("CREATE TABLE " + uname + " (id INTEGER PRIMARY KEY, note TEXT, day TEXT, date TEXT, time TEXT) ")
    dbnotes.commit()


def encode(uname, password):
    n = random.randint(1, 1001)
    new = ""

    for i in range(0, len(password)):
        h = ord(password[i])
        new += chr(h + n)

    new = str(n + len(uname)) + "!" + new
    return new


def decode(uname, password):
    l = len(uname)
    q = (password.index('!'))
    s = int(password[2:q])
    s -= l
    password = password[q + 1:len(password) - 3]
    new = ""

    for i in range(0, len(password)):
        new += (chr(ord(password[i]) - s))
    return new


def checkuname(uname):
    dbusers = sqlite3.connect("users.db")
    cu = dbusers.cursor()
    cu.execute("SELECT uname FROM users")
    l = list(cu.fetchall())
    length = len(l)

    for i in range(0, length):
        s = str(l[i])
        s = s[2:len(s) - 3]
        if uname.lower() == s.lower():
            return True


def checkHelper(uname, password, encrypt):
    global dpass1, alerttext
    dbusers = sqlite3.connect("users.db")
    cu = dbusers.cursor()

    if checkuname(uname):
        dpass = str(cu.execute('SELECT pass FROM users WHERE uname = "' + uname + '"').fetchone())
        dpass1 = dpass
        if not encrypt:
            dpass = decode(uname, dpass)

        if password in dpass:
            status = True

        else:
            status = False
            alerttext = "Error - Incorrect Password"

    else:
        status = False
        alerttext = "Error - Incorrect Username"

    return status


def add(uname, note):
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    time1 = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    day = datetime.datetime.fromtimestamp(time.time()).strftime('%A')
    insertNote(uname, note, day, date, time1)


def insertNote(uname, note, day, date, time):
    dbnotes = sqlite3.connect("notes.db")
    cn = dbnotes.cursor()
    cn.execute("INSERT INTO " + uname + "(note, day, date, time) VALUES (?, ?, ?, ?)", (note, day, date, time))
    dbnotes.commit()


def deleteNote(uname, note):
    dbnotes = sqlite3.connect("notes.db")
    cn = dbnotes.cursor()
    id = str(cn.execute("SELECT id FROM " + uname + " WHERE note = \"" + note + "\"").fetchone())
    id = id[1: len(id) - 2]
    # print(id)
    cn.execute("DELETE FROM " + uname + " WHERE note = \"" + note + "\"")
    cn.execute("UPDATE " + uname + " SET ID = ID-1 WHERE ID > " + id)
    dbnotes.commit()


def updateNote(uname, oldnote, newnote):
    dbnotes = sqlite3.connect("notes.db")
    cn = dbnotes.cursor()
    id = str(cn.execute("SELECT id FROM " + uname + " WHERE note = \"" + oldnote + "\"").fetchone())
    id = id[1: len(id) - 2]
    cn.execute("UPDATE " + uname + " SET note = \"" + newnote + "\" WHERE id = " + id)
    dbnotes.commit()


# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return 'You want path: %s' % path

@app.route("/about", methods=['post', 'get'])
def about():
    return render_template("about.html")


@app.route("/", methods=['post', 'get'])
def index():
    return render_template("index.html")


@app.route("/login", methods=['post', 'get'])
def login():
    return render_template("login.html")


@app.route("/newacc", methods=['post', 'get'])
def newacc():
    return render_template("newacc.html")


@app.route("/jlogin", methods=['post'])
def jlogin():
    global dpass1, alerttext
    uname = str(request.form["username"]).lower()
    password = str(request.form['password'])

    status = checkHelper(uname, password, False)
    local, alerttext = alerttext, ""
    return jsonify(status=status, alert=local, uname=uname, password=dpass1)


@app.route("/jnewacc", methods=['post'])
def jnewacc():
    global alerttext
    fname = str(request.form["fname"])
    lname = str(request.form["lname"])
    email = str(request.form["email"])
    phone = str(request.form["phone"])
    uname = str(request.form["username"]).lower()
    password = str(request.form["password"])
    sques = str(request.form["sques"])
    ans = str(request.form["ans"])
    if not checkuname(uname):
        password = encode(uname, password)
        ans = encode(uname, ans)
        insertNewAcc(fname, lname, email, phone, uname, password, sques, ans)
        createTable(uname)
        status = True
        color = "green"
    else:
        alerttext = "Username already taken"
        color = "red"
        status = False

    local, alerttext = alerttext, ""
    return jsonify(status=status, alerttext=local, color=color, uname=uname, password=password)


@app.route("/main/<uname>", methods=['get', 'post'])
def main(uname):
    dbnotes = sqlite3.connect("notes.db")
    cn = dbnotes.cursor()
    notes = []
    dates = []
    cn.execute('SELECT id, note, day, date, time FROM "' + uname + '"')

    for i in cn.fetchall():
        notes.append(i[1])
        dates.append(i[2] + " : " + i[3] + " : " + i[4])
    return render_template('main.html', notes=notes, dates=dates)


@app.route("/jmain", methods=['post', 'get'])
def jmain():
    uname = str(request.form['username']).lower()
    password = str(request.form['password'])
    link = str(request.form['link'])

    n = int(link.rfind('/'))
    link = link[n + 1:]

    # print(uname + " " + password + " " + link)

    if uname != "none" and password != "None" and link == uname:
        status = checkHelper(uname, password, True)
    else:
        status = False

    return jsonify(status=status)


@app.route("/jaddNote", methods=['post', 'get'])
def jaddNote():
    note = str(request.form['note'])
    uname = str(request.form['username'])
    add(uname, note)
    status = True

    return jsonify(status=status, uname=uname)


@app.route("/jdeleteNote", methods=['post', 'get'])
def jdeleteNote():
    note = str(request.form['note'])
    uname = str(request.form['username'])

    deleteNote(uname, note)

    return jsonify(status=True, uname=uname)


@app.route('/jeditNote', methods=['get', 'post'])
def jeditNote():
    oldnote = str(request.form['oldnote'])
    newnote = str(request.form['newnote'])
    uname = str(request.form['username'])

    updateNote(uname, oldnote, newnote)

    return jsonify(status=True, uname=uname)


app.run(debug=False)

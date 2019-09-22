# TODO: Read about Ajax
# TODO: PL/SQL for password, email, phone verification
# TODO: Add category option, lower it and save it. while displaying, display first letter capital
# TODO: in if_username_exists(), make better quesry to get empty list or uname list

from flask import Flask, render_template, request, redirect
import matplotlib
import mysql.connector
import datetime
import calendar
import random
import json


db_diary = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root123",
  database="diary")
cur_diary = db_diary.cursor()
app = Flask(__name__)

# "INSERT INTO users(firstname, lastname, email, phone_number, username, password, security_ques, security_ans) VALUES ("Aditi", "", "a@g.c", "1234567890", "aditisri", "lolol12345", "crush?", "lol");
def validate_password(password): 
    alert_text = ""
    special_symbols =['$', '@', '#', '%', '_'] 
    is_valid = True
      
    if len(password) < 8: 
        alert_text += ('Length should be at least 8<br>') 
        is_valid = False
          
    if not any(char.isdigit() for char in password): 
        alert_text += ('Password should have at least one numeral<br>') 
        is_valid = False
          
    if not any(char.isupper() for char in password): 
        alert_text += ('Password should have at least one uppercase letter<br>') 
        is_valid = False
          
    if not any(char.islower() for char in password): 
        alert_text += ('Password should have at least one lowercase letter<br>') 
        is_valid = False
          
    if not any(char in special_symbols for char in password): 
        alert_text += ('Password should have at least one of the symbols $ @ # % _ <br>') 
        is_valid = False
    
    return {"is_valid" : is_valid, "alert_text" : alert_text} 
def encode(password):
    n = random.randint(1, 11)
    new = ""

    for i in range(0, len(password)):
        new += chr(ord(password[i]) + n)
    return str(n) + "!" + new
def decode(password):
    q = (password.index('!'))
    s = int(password[:q])
    password = password[q+1:]
    new = ""

    for i in range(0, len(password)):
        new += (chr(ord(password[i]) - s))
    return new
def if_username_exists(uname):
    cur_diary.execute("SELECT username FROM users")
    l = (cur_diary.fetchall())

    for i in l:
        if uname == i[0]:
            return True
    return False
def insert_newacc(fname, lname, email, phone, uname, password, sques, ans):
    cur_diary.execute(
        "INSERT INTO users(firstname, lastname, email, phone_number, username, password, security_ques, security_ans) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)",
        (fname, lname, email, phone, uname, str(password), sques, str(ans)))
    db_diary.commit()
def create_user_table(uname):
    cur_diary.execute(f"CREATE TABLE user_{uname} (id INTEGER PRIMARY KEY AUTO_INCREMENT, category TEXT NOT NULL, note TEXT NOT NULL, date_time datetime NOT NULL) ")
    db_diary.commit()
    cur_diary.execute(f'SELECT id FROM users WHERE username="{uname}"')
    cur_diary.execute(f'INSERT INTO login_count (id) VALUES ({int(cur_diary.fetchone()[0])})')
    db_diary.commit()
def insert_note(uname, category, note):
    cur_diary.execute("SELECT NOW();")
    date_time = cur_diary.fetchone()[0]
    cur_diary.execute(f"INSERT INTO user_{uname} (category, note, date_time) VALUES (%s, %s, %s)", (category, note, date_time))
    db_diary.commit()
def delete_note(uname, note):
    cur_diary.execute(f"SELECT id FROM user_{uname} WHERE note = \"{note}\"")
    id = str(cur_diary.fetchone()[0])
    cur_diary.execute(f"DELETE FROM user_{uname} WHERE note = \"{note}\"")
    cur_diary.execute(f"UPDATE user_{uname} SET ID = ID-1 WHERE ID > {id}")
    db_diary.commit()
def update_note(uname, oldnote, newnote):
    cur_diary.execute(f"UPDATE user_{uname} SET note = \"{newnote}\" WHERE note = \"{oldnote}\"")
    db_diary.commit()
def verify_password(uname, password):
    values = {"status" : True, "alert_text" : ""}
    uname = uname.lower()
    if if_username_exists(uname):
        cur_diary.execute(f'SELECT password FROM users WHERE username = "{uname}"')
        database_password = decode(str(cur_diary.fetchone()[0]))

        if not password == database_password:
            values["status"] = False
            values["alert_text"] = "Error - Incorrect Password"

    else:
        values["status"] = False
        values["alert_text"] = "Error - Incorrect Username"

    return values
def increment_logincount(uname):
    cur_diary.execute(f'SELECT id FROM users WHERE username="{uname}"')
    id = cur_diary.fetchone()[0]
    cur_diary.execute(f'SELECT count FROM login_count WHERE id={id}')
    cur_diary.execute(f'UPDATE login_count SET count={int(cur_diary.fetchone()[0]) + 1} WHERE id={id}')
    db_diary.commit()
    

@app.route("/", methods=['post', 'get'])
def index():
  return render_template('index.html')

@app.route("/about", methods=['post', 'get'])
def about():
    return render_template("about.html")

@app.route("/login", methods=['post', 'get'])
def login():
    return render_template("login.html")

@app.route("/newacc", methods=['post', 'get'])
def newacc():
    return render_template("new_account.html")

@app.route("/ajax_validate_newacc", methods=['post'])
def ajax_validate_newacc():
    fname = str(request.form["fname"])
    lname = str(request.form["lname"])
    email = str(request.form["email"])
    phone = str(request.form["phone"])
    uname = str(request.form["username"]).lower()
    password = str(request.form["password"])
    sques = str(request.form["sques"])
    ans = str(request.form["ans"])

    username_taken = if_username_exists(uname)
    valid_password = validate_password(password)

    values = {"status" : True, "alert_text" : "", "color" : "green", "uname" : uname, "password" : password}

    if not username_taken and valid_password["is_valid"]:
        password = encode(password)
        ans = encode(ans)
        insert_newacc(fname, lname, email, phone, uname, password, sques, ans)
        create_user_table(uname)
        values["password"] = password
        return json.dumps(values)

    if username_taken:
        values["alert_text"] = "Username already taken"
    elif not valid_password["is_valid"]:
        values["alert_text"] = valid_password["alert_text"]

    values["color"] = "red"
    values["status"] = False
    return json.dumps(values)

@app.route("/ajax_validate_login", methods=['post'])
def ajax_validate_login():
    uname = str(request.form["username"]).lower()
    password = str(request.form['password'])

    values = verify_password(uname, password)
    values.update({"uname" : uname, "password" : encode(password)})

    if values['status']:
        increment_logincount(uname)
    return json.dumps(values)

@app.route("/main/<uname>", methods=['get', 'post'])
def main_username(uname):
    notes, dates, category = [], [], []
    cur_diary.execute(f'SELECT * FROM user_{uname}')
    database_data = cur_diary.fetchall()

    for item in database_data:
        category.append(item[1])
        notes.append(item[2])
        dates.append(str(calendar.day_name[item[3].date().weekday()]) + " : " + str(item[3].date()) + " : " + str(item[3].time()))
    return render_template('main.html', category=category, notes=notes, dates=dates)

@app.route("/ajax_main", methods=['post', 'get'])
def ajax_main():
    values = {'status': True, 'alert_text': ''}
    uname = str(request.form['username']).lower()
    password = str(request.form['password'])
    link = str(request.form['link'])
    link = link[int(link.rfind('/')) + 1:]

    # print(uname + " " + password + " " + link)

    if uname != "none" and password != "None" and link == uname:
        values = verify_password(uname, decode(password))
    else:
        values["status"] = False

    return json.dumps(values)

@app.route("/ajax_add_note", methods=['post', 'get'])
def ajax_add_note():
    category = str(request.form['category'])
    # category = "College"
    note = str(request.form['note'])
    uname = str(request.form['username'])
    insert_note(uname, category, note)

    return json.dumps({"status" : True, "username" : uname})

@app.route("/ajax_delete_note", methods=['post', 'get'])
def ajax_delete_note():
    note = str(request.form['note']).strip()
    uname = str(request.form['username'])
    delete_note(uname, note)
    return json.dumps({"status" : True, "username" : uname})

@app.route('/ajax_edit_note', methods=['get', 'post'])
def ajax_edit_note():
    oldnote = str(request.form['oldnote']).strip()
    newnote = str(request.form['newnote'])
    uname = str(request.form['username'])
    update_note(uname, oldnote, newnote)

    return json.dumps({"status" : True, "username" : uname})

app.run(debug=True)
# increment_logincount('yesaditi1')
# insert_newacc('lol', 'lol', 'lol', '98765431134', 'lol9', 'test', 'sed', 'yes')
# create_user_table("lol9")
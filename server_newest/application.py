# TODO: Read about Ajax
# TODO: PL/SQL for password, email, phone verification
# TODO: check delete id ka

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime
import calendar
import random
import json

global_selected_subject = ""
global_selected_year = ""
global_selected_branch = ""
notes, dates, category, faculty = [], [], [], [] # VERY BAD. THINK AN ALTERNATIVE PLEASE
# CREATE TABLE users(id INTEGER PRIMARY KEY AUTO_INCREMENT, firstname varchar(20) NOT NULL, lastname varchar(20), email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, security_ques TEXT NOT NULL, security_ans TEXT NOT NULL);
# CREATE TABLE notes(id INTEGER PRIMARY KEY AUTO_INCREMENT, category_id varchar(20), notes text, date_time datetime)

database = mysql.connector.connect(
  host="localhost", 
  user="root",  
  passwd="root123",
  database="notes_management_system_db",
  autocommit=True)
cursor = database.cursor()
app = Flask(__name__)

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
    if len(l) > 0:
        return True
def if_username_exists(uname):
    cursor.execute(f'SELECT username FROM users WHERE username="{uname}"')
    l = (cursor.fetchall())

    if len(l) > 0:
        return True
    return False
def insert_newacc(fname, lname, email, phone, uname, password, sques, ans, acc_type):
    cursor.execute(
        "INSERT INTO users(firstname, lastname, email, username, password, security_ques, security_ans, account_type) VALUES (%s, %s, %s, %s, %s, %s ,%s, %s)",
        (fname, lname, email, uname, str(password), sques, str(ans), str(acc_type)))

    cursor.execute(f'SELECT id FROM users WHERE username="{uname}"')
    cursor.execute(f'INSERT INTO login_count (id) VALUES ({int(cursor.fetchone()[0])})')
def insert_note(uname, category, note):
    global global_selected_year, global_selected_subject, global_selected_branch
    cursor.execute("SELECT NOW();")
    date_time = cursor.fetchone()[0]

    cursor.execute(f'select id from users where username="{uname}"')
    id = cursor.fetchone()[0]

    if global_selected_year != "" and global_selected_subject != "":
        cursor.execute(f'select id from engg_{global_selected_branch}_{global_selected_year} where Subjects="{global_selected_subject}"')
        sub_id = cursor.fetchone()[0]
        branch = ""
        if global_selected_branch == "computers":
            branch = "comp"
        elif global_selected_branch == "mechanical":
            branch = "mech"

        cursor.execute(f"INSERT INTO notes (unit, notes, date_time, subject_id, category_id, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
         (category, note, date_time, sub_id, f'engg_{branch}_{global_selected_year.lower()}', id))
        return True
    return False
def delete_note(uname, note):
    cursor.execute(f"SELECT id FROM notes WHERE notes = \"{note}\"")
    id = str(cursor.fetchone()[0])
    cursor.execute(f"DELETE FROM notes WHERE notes = \"{note}\"")
    cursor.execute(f"UPDATE notes SET ID = ID-1 WHERE ID > {id}")
def update_note(uname, oldnote, newnote, newcat):
    cursor.execute(f"UPDATE notes SET notes = \"{newnote}\", unit = \"{newcat}\" WHERE notes = \"{oldnote}\"")
def verify_password(uname, password):
    values = {"status" : True, "alert_text" : ""}
    uname = uname.lower()
    if if_username_exists(uname):
        cursor.execute(f'SELECT password FROM users WHERE username = "{uname}"')
        database_password = decode(str(cursor.fetchone()[0]))

        if not password == database_password:
            values["status"] = False
            values["alert_text"] = "Error - Incorrect Password"

    else:
        values["status"] = False
        values["alert_text"] = "Error - Incorrect Username"

    return values
def increment_logincount(uname):
    cursor.execute(f'SELECT id FROM users WHERE username="{uname}"')
    id = cursor.fetchone()[0]
    cursor.execute(f'SELECT count FROM login_count WHERE id={id}')
    cursor.execute(f'UPDATE login_count SET count={int(cursor.fetchone()[0]) + 1} WHERE id={id}')
    
@app.before_request
def before_request_func():
    if request.path.split('/')[1] == 'main':
        values = {'status': True, 'alert_text': ''}
        uname = request.cookies.get('username')
        password = request.cookies.get('password')
        link = request.path
        link = link[int(link.rfind('/')) + 1:]

        # print(str(uname) + " " + str(password) + " " + link)

        if uname != "none" and password != "None" and link == uname:
            values = verify_password(uname, decode(password))
        else:
            values["status"] = False
            return redirect('/login')

@app.route("/", methods=['post', 'get'])
def index():
  return render_template('index.html')

@app.route("/about", methods=['post', 'get'])
def about():
    return render_template("about.html")

@app.route("/login", methods=['post', 'get'])
def login():
    global notes, dates, category
    notes, dates, category = [], [], []
    return render_template("new-login.html")

@app.route("/newacc", methods=['post', 'get'])
def newacc():
    global notes, dates, category
    notes, dates, category = [], [], []

    return render_template("new-newacc.html")

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
    account_type = (str(request.form["account_type"]))

    username_taken = if_username_exists(uname)
    valid_password = validate_password(password)

    values = {"status" : True, "alert_text" : "", "color" : "green", "uname" : uname, "password" : password, "account_type" : account_type}

    if not username_taken and valid_password["is_valid"]:
        password = encode(password)
        ans = encode(ans)
        insert_newacc(fname, lname, email, phone, uname, password, sques, ans, account_type)
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

    cursor.execute(f'select account_type from users where username="{uname}"')
    values.update({"uname" : uname, "password" : encode(password)})

    values["account_type"] =  cursor.fetchone()[0]
    print(values)
    if values['status']:
        increment_logincount(uname)
    return json.dumps(values)

@app.route("/main/<uname>", methods=['get', 'post'])
def main_username(uname):
    global global_selected_subject, global_selected_year, global_selected_branch
    global notes, dates, category, faculty

    if request.method == 'POST':
        notes, dates, category, faculty = [], [], [], []
        cursor.execute(f'select id from engg_{global_selected_branch}_{global_selected_year} where Subjects="{global_selected_subject}"')
        subj_id = cursor.fetchone()[0]

        cursor.execute(f'select id from users where username="{uname}"')
        user_id = cursor.fetchone()[0]

        branch = ""
        if global_selected_branch == "computers":
            branch = "comp"
        elif global_selected_branch == "mechanical":
            branch = "mech"

        cursor.execute(f'SELECT * from notes where subject_id="{subj_id}" AND category_id="engg_{branch}_{global_selected_year}"')

        data = cursor.fetchall()
        for item in data:
            cursor.execute(f'SELECT username FROM users WHERE id="{item[6]}"')
            faculty.append(cursor.fetchone()[0])
            category.append('UNIT ' + str(item[5]))
            notes.append(item[2])
            dates.append(str(calendar.day_name[item[3].date().weekday()]) + " : " + str(item[3].date()) + " : " + str(item[3].time()))

    return render_template('main.html', category=category, notes=notes, dates=dates, faculty=faculty)

@app.route("/ajax_add_note", methods=['post', 'get'])
def ajax_add_note():
    category = str(request.form['category']).lower()
    note = str(request.form['note'])
    uname = str(request.form['username'])
    return json.dumps({"status" : insert_note(uname, category, note), "username" : uname})

@app.route("/ajax_delete_note", methods=['post', 'get'])
def ajax_delete_note():
    note = str(request.form['note']).strip()
    uname = str(request.cookies.get('username'))
    delete_note(uname, note)
    return json.dumps({"status" : True, "username" : uname})

@app.route('/ajax_edit_note', methods=['get', 'post'])
def ajax_edit_note():
    oldnote = str(request.form['oldnote']).strip()
    newnote = str(request.form['new_note'])
    newcat = str(request.form['newcat']).lower()
    uname = str(request.cookies.get('username'))

    print(uname, oldnote, newnote, newcat)
    update_note(uname, oldnote, newnote, newcat)
    return json.dumps({"status" : True, "username" : uname})

@app.route('/ajax_get_subjects', methods=['get', 'post'])
def ajax_get_subjects():
    global global_selected_year, global_selected_branch
    global_selected_year = str(request.form['year']).upper()
    cursor.execute(f'SELECT Subjects FROM engg_{global_selected_branch}_{global_selected_year};')
    db_list = cursor.fetchall()
    
    subject_list = ["Select Subject"]
    for i in db_list:
        subject_list.append(i[0])

    return json.dumps({"status": True, "subject_list": subject_list})

@app.route('/ajax_set_branch', methods=['post'])
def ajax_set_branch():
    global global_selected_branch

    global_selected_branch = str(request.form['branch'])
    return json.dumps({})

@app.route('/ajax_get_notes', methods=['get', 'post'])
def ajax_get_notes():
    global global_selected_subject
    global_selected_subject = str(request.form['subject'])
    return json.dumps({"status": True})
    
app.run(debug=True)
# increment_logincount('yesaditi1')
# insert_newacc('lol', 'lol', 'lol', '98765431134', 'lol9', 'test', 'sed', 'yes')
# create_user_table("lol9")
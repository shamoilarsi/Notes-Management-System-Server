import sqlite3
import datetime
import time
import random

dbnotes = sqlite3.connect('notes.db')
dbusers = sqlite3.connect('users.db')
cn = dbnotes.cursor()
cu = dbusers.cursor()

intro = "     ~~~~~Die-ary~~~~~     \n\n"

# CREATE TABLE users(id INTEGER PRIMARY KEY AUTO_INCREMENT, firstname varchar(20) NOT NULL, lastname varchar(20), email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, security_ques TEXT NOT NULL, security_ans TEXT NOT NULL);
# cu.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, email TEXT, uname TEXT, pass TEXT, sques TEXT, ans TEXT)")

def insertNewAcc(fname, lname, email, uname, password, sques, ans):
    cu.execute("INSERT INTO users(firstname, lastname, email, uname, pass, sques, ans) VALUES (?, ?, ?, ?, ?, ? ,?)",
               (fname, lname, email, uname, password, sques, ans))
    dbusers.commit()


def createTable(uname):
    cn.execute("CREATE TABLE " + uname + "(id INTEGER PRIMARY KEY, note TEXT, day TEXT, date TEXT, time TEXT) ")
    dbnotes.commit()


def insertNote(uname, note, day, date, time):
    cn.execute("INSERT INTO " + uname + "(note, day, date, time) VALUES (?, ?, ?, ?)", (note, day, date, time))
    dbnotes.commit()


def deleteNote(uname, n):
    cn.execute("DELETE FROM " + uname + " WHERE id = " + n)
    cn.execute("UPDATE " + uname + " SET ID = ID-1 WHERE ID > " + n)
    dbnotes.commit()


def updateNote(uname, note, n):
    cn.execute("UPDATE " + uname + " SET note = \"" + note + "\" WHERE id = " + n)
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


def checkEmail(email):
    if '@' in email and '.' in email:
        return True
    else:
        return False


def start():
    print(intro)
    c = int(input('Enter "1" for Login,\nEnter "2" for New User,\nEnter "3" to Exit.\nEnter Choice - '))
    if c == 1:
        login()
    elif c == 2:
        newAcc()
    elif c == 3:
        close()


def changeEmail(uname):
    newemail = str(input("Enter new Email - "))
    if checkEmail(newemail):
        cu.execute("UPDATE users SET email = \"" + newemail + "\" WHERE uname = \"" + uname + "\"")
        dbusers.commit()
        input("Email updated. Press Enter to continue")
        displayNotes(uname)
    else:
        op1 = input("Invalid Email. Try another email.\nPress '1' to try again,\nPress '2' to Exit.\nEnter Choice - ")
        if op1 == '1':
            changeEmail(uname)
        elif op1 == '2':
            displayNotes(uname)


def checkuname(uname, t):
    cu.execute("SELECT uname FROM users")
    l = list(cu.fetchall())
    length = len(l)

    for i in range(0, length):
        s = str(l[i])
        s = s[2:len(s) - 3]
        if uname == s:
            return True


def add(uname):
    note = input("Enter Note - \n")
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    time1 = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    day = datetime.datetime.fromtimestamp(time.time()).strftime('%A')
    insertNote(uname, note, day, date, time1)
    input("Note Added.\nEnter any key to view all notes\n")
    displayNotes(uname)


def delete(uname):
    n = input("Enter id of note to be deleted - ")
    deleteNote(uname, n)
    input("Note Deleted.\nEnter any key to view all notes\n")
    displayNotes(uname)


def update(uname):
    n = input("Enter id of note to be updated - ")
    note = input("Enter the updated note - \n")
    updateNote(uname, note, n)
    input("Note Updated.\nEnter any key to view all notes\n")
    displayNotes(uname)


def userChange(uname):
    dpass = str(cu.execute('SELECT pass FROM users WHERE uname = "' + uname + '"').fetchone())
    # ans = str(cu.execute('SELECT ans FROM users WHERE uname = "' + uname + '"').fetchone())
    password = dpass[2: len(dpass) - 3]
    # ans = ans[2:len(ans) - 3]
    dpass = decode(uname, dpass)
    # ans = decode(uname, ans)
    newuname = input("Enter New Username - ")
    if not checkuname(newuname, 3):
        newdpass = encode(newuname, dpass)
        # newans = encode(newuname, ans)
        cu.execute(
            "UPDATE users SET uname = \"" + newuname + "\", pass = \"" + newdpass + "\" WHERE pass = \"" + password + "\"")
        dbusers.commit()
        cn.execute("ALTER TABLE " + uname + " RENAME TO " + newuname)
        dbusers.commit()
        input("Username changed. Press Enter to continue")
        displayNotes(newuname)
    else:
        c = input("Username alerady exists. \nPress '1' to try again,\nPress '2' to exit.\nEnter Choice - ")
        if c == '1':
            userChange(uname)
        elif c == '2':
            displayNotes(uname)


def passChange(uname):
    newpass = input("\nEnter new Password - ")
    newpass = encode(uname, newpass)
    cu.execute("UPDATE users SET pass = \"" + newpass + "\" WHERE uname = \"" + uname + "\"")
    dbusers.commit()
    input("Password Changed. Press enter to display notes")
    displayNotes(uname)


def forgotpass(uname):
    sques = str(cu.execute("SELECT sques FROM users WHERE uname = \"" + uname + "\"").fetchone())
    ans = input(sques[2:len(sques) - 3] + " - ")
    dans = str(cu.execute("SELECT ans FROM users WHERE uname = \"" + uname + "\"").fetchone())
    dans = decode(uname, dans)
    if ans.lower() == dans.lower():
        passChange(uname)

    else:
        op = input(
            "Entered answer does not match with the answer in database.\nPress '1' to answer security question again,"
            "\nPress '2' to exit.\nEnter choice - ")
        if op == '1':
            forgotpass(uname)
        elif op == '2':
            start()


def login():
    # os.system('cls')
    print(intro)
    print("Login Page - \n")
    uname = input("Enter Username - ")
    if checkuname(uname, 1):
        password = input("Enter Password - ")
        dpass = str(cu.execute('SELECT pass FROM users WHERE uname = "' + uname + '"').fetchone())
        dpass = decode(uname, dpass)
        if password in dpass:
            # os.system('cls')
            displayNotes(uname)
        else:
            op = input(
                "Password does not match.\nPress '1' to login again,\nPress '2' if you don't remember your "
                "password.\nEnter choice - ")
            if op == '1':
                login()
            elif op == '2':
                forgotpass(uname)

    else:
        q = int(input(
            "Username does not exist in database. \n\nPress '1' to create new account.\nPress '2' to retry login\n"))
        if q == 1:
            newAcc()
        elif q == 2:
            login()


def newAcc():
    # os.system('cls')
    print(intro)
    print("Create New Account -  \n")
    firstname = input("Enter First name - ")
    lastname = input("Enter Last name - ")
    email = input("Enter Email - ")

    if checkEmail(email):
        uname = input("Enter Username - ")
        if not checkuname(uname, 2):
            password = input("Enter Password - ")
            password = encode(uname, password)
            sques = input("Enter a Security Question of your choice - ")
            ans = input("Enter answer for the above entered question - ")
            ans = encode(uname, ans)
            insertNewAcc(firstname, lastname, email, uname, password, sques, ans)
            createTable(uname)
            print("Account Created\nPress any key to Login")
            input()
            login()
        else:
            q = int(input("Username already exists. \n\nPress '1' to enter different Username.\nPress '2' to login\n"))
            if q == 1:
                newAcc()
            elif q == 2:
                login()

    else:
        op1 = input("Invalid Email. Try another email.\nPress '1' to try again,\nPress '2' to Exit.\nEnter Choice - ")
        if op1 == '1':
            newAcc()
        elif op1 == '2':
            start()


def close():
    # os.system('cls')
    print("\nProgram will end in 3 seconds. Hope to see you again!")
    cn.close()
    cu.close()
    dbnotes.close()
    dbusers.close()
    time.sleep(3)


def settings(uname):
    op1 = input("""\nPress 'U' to change Username,\nPress 'P' to change Password,\nPress 'E' to change Email,
    \nPress 'C' to Cancel.\nEnter option - """)
    if op1 == 'u' or op1 == 'U':
        userChange(uname)
    elif op1 == 'p' or op1 == 'P':
        oldpass = input("Enter old Password - ")
        olddpass = str(cu.execute("SELECT pass FROM users WHERE uname = \"" + uname + "\"").fetchone())
        olddpass = decode(uname, olddpass)
        if oldpass == olddpass:
            passChange(uname)
        else:
            op = input("Password does not match.\nPress '1' to try again,\nPress '2' to cancel.\nEnter Choice - ")
            if op == '1':
                passChange(uname)
            elif op == '2':
                displayNotes(uname)
    elif op1 == 'e' or op1 == 'E':
        changeEmail(uname)

    elif op1 == 'c' or op1 == 'C':
        displayNotes(uname)


def search(uname):
    op = input("Press '1' to search be query,\nPress '2' to search by date.\nEnter choice - ")
    if op == '1':
        q = input("Enter Query to be searched - ")
        print("These are the notes that match your query - \n")
        all = cn.execute("SELECT id, note, day, date FROM " + uname).fetchall()
        l = len(all)
        for i in range(0, l):
            if q in all[i][1]:
                print(str(all[i][0]) + " - " + all[i][1] + "\n    - " + all[i][2] + " : " + all[i][3] + "\n")

        a = input("Press '1' to Search another query,\nPress '2' to display all notes.\nEnter Choice - ")
        if a == '1':
            search(uname)
        elif a == '2':
            displayNotes(uname)

    elif op == '2':
        q = input("Enter date to be searched (YYYY-MM-DD)- ")
        print("These are the notes that match your query - \n")
        all = cn.execute("SELECT id, note, day, date FROM " + uname).fetchall()
        l = len(all)
        for i in range(0, l):
            if q == all[i][3]:
                print(str(all[i][0]) + " - " + all[i][1] + "\n    - " + all[i][2] + " : " + all[i][3] + "\n")
        a = input("Press '1' to Search another query,\nPress '2' to display all notes.\nEnter Choice - ")
        if a == '1':
            search(uname)
        elif a == '2':
            displayNotes(uname)


def filt(uname):
    d1 = input("Enter earlier date (YYYY-MM-DD) - ")
    d2 = input("Enter latter date (YYYY-MM-DD) - ")
    print("These are the notes after filtering - \n")
    all = cn.execute("SELECT id, note, day, date FROM " + uname).fetchall()
    l = len(all)
    for i in range(0, l):
        if d1 <= all[i][3] <= d2:
            print(str(all[i][0]) + " - " + all[i][1] + "\n    - " + all[i][2] + " : " + all[i][3] + "\n")
    a = input("Press '1' to Search another query,\nPress '2' to display all notes.\nEnter Choice - ")
    if a == '1':
        search(uname)
    elif a == '2':
        displayNotes(uname)


def displayNotes(uname):
    # os.system('cls')
    print(intro)
    print("Welcome to Die-ary\nHere is a list of all your notes - \n")
    cn.execute("SELECT id, note, day, date, time FROM " + uname)

    for i in cn.fetchall():
        print(str(i[0]) + " - " + i[1] + "\n    - " + i[2] + " : " + i[3] + " : " + i[4] + "\n")

    op1 = input(
        """\nPress 'A' to Add a note, \nPress 'D' to Delete a note, \nPress 'U' to Update a note,\nPress 'Q' to Search,\nPress 'F' to Filter notes,\nPress 'S' for Settings,\nPress 'N' to Log off.\nEnter option - """)

    if op1 == 'A' or op1 == 'a':
        add(uname)
    elif op1 == 'D' or op1 == 'd':
        delete(uname)
    elif op1 == 'U' or op1 == 'u':
        update(uname)
    elif op1 == 'N' or op1 == 'n':
        start()
    elif op1 == 'S' or op1 == 's':
        settings(uname)
    elif op1 == 'Q' or op1 == 'q':
        search(uname)
    elif op1 == 'F' or op1 == 'f':
        filt(uname)


start()


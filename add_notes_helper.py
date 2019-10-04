import mysql.connector
import random

database = mysql.connector.connect(
  host="localhost", 
  user="root",  
  passwd="root123",
  database="notes_management_system_db",
  autocommit=True)
cursor = database.cursor()

list_branches = ['comp', 'mech']
list_table = ['computers', 'mechanical']
list_year = ['SE', 'TE', 'BE']

list_user_id = [1, 3, 5]
list_subject_id = [1, 2, 3, 4, 5, 6]


for i in range(200):
    cursor.execute("SELECT NOW();")
    date_time = cursor.fetchone()[0]

    id_subject = random.choices(list_subject_id)[0]
    id_user = random.choices(list_user_id)[0]
    id_year = random.choices(list_year)[0]
    id_branch = random.randint(0, 1)

    cursor.execute(f'select Subjects from engg_{list_table[id_branch]}_{id_year} where id={id_subject}')
    subject_name = cursor.fetchone()[0]

    cursor.execute(f"INSERT INTO notes (unit, notes, date_time, subject_id, category_id, user_id) VALUES (%s, %s, %s, %s, %s, %s)", 
    (random.choices(list_subject_id)[0], f"This is a note from {subject_name} {i}", date_time, id_subject,
    f'engg_{list_branches[id_branch]}_{id_year.lower()}', id_user))

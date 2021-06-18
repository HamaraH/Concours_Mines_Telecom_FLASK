import sys
sys.path.append("..")
import main
import random
import string

def createAccount(mail, password):

    db = main.get_db()
    db.execute(''' INSERT INTO COMPTE (login, password) VALUES (?,?)''',
                     (mail, password))
    db.commit()

def accountExists(login, password):

    db = main.get_db()
    result = db.execute(''' SELECT * FROM COMPTE AS C WHERE C.login = ? AND C.password = ?''', (login, password))

    rows = result.fetchall()
    if rows == []:
        return False
    else:
        return True
 

def createStudentsAccounts():

    db = main.get_db()

    test = db.execute('''SELECT COUNT(*) FROM COMPTE ''')
    test_row = test.fetchall()

    if test_row[0][0] == 0:

        results1 = db.execute(''' SELECT can_cod FROM ELEVE ''')
        results2 = db.execute(''' SELECT can_cod FROM ATS ''')
        rows1 = results1.fetchall()
        rows2 = results2.fetchall()

        rows = rows1 + rows2

        length = 8
        all = string.ascii_letters + string.digits + string.punctuation

        for row in rows:
            can_cod = row[0]
            passw = "".join(random.sample(all, length))
            db.execute(''' INSERT INTO COMPTE (login, password) VALUES (?,?)''',
                       (can_cod, passw))

        db.commit()


def isEmpty():

    db = main.get_db()
    result = db.execute(''' SELECT COUNT (*) FROM COMPTE''')

    rows = result.fetchall()

    if rows[0][0] > 0:
        return False
    else:
        return True

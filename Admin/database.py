import sqlite3 as sql
from sqlite3.dbapi2 import DatabaseError

from passlib.hash import sha256_crypt as shc

def sql_connection():
    try:
        conn = sql.connect('admino.db')
        return conn
    except :
        raise ConnectionError('Unable to connect to database')
    

def create_account(conn, userid, password):
    if not (isinstance(userid, str) and isinstance(password, str)):
        raise TypeError('args must be of string type')
    else:
        password = shc.hash(password)
        cursor = conn.cursor()
        cursor.execute(
            '''
            insert into users(userID, password) values (?, ?)
            ''',
            (userid, password)
        )
        conn.commit()
        conn.close()

    
def create_UserTable(conn):
    cursor = conn.cursor()

    cursor.execute(
        '''
        create table users(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            userID TEXT NOT NULL,
            password TEXT NOT NULL
        );
        '''
    )
    conn.commit()
    conn.close()


def create_CustomTable(conn, table_name):
    if isinstance(table_name, str):
        cursor = conn.cursor()
        cursor.execute(
            f'''
            drop table if exists {table_name}
            '''
        )
        cursor.execute(
            f'''
            create table {table_name}(
                id integer auto_increment not null,
                question text not null,
                image BLOB,
                optionA text,
                optionB text,
                optionC text,
                optionD text,
                answer varchar(1)
            )
            '''
        )
    conn.commit()
    conn.close()


def delete_CustomTable(conn, table_name):
    if isinstance(table_name, str):
        cursor = conn.cursor()
        cursor.execute(
            f'''
            DROP TABLE {table_name}
            '''
        )
    conn.commit()
    conn.close()


def deleteAll_CustomTable(conn, table_names):
    for table_name in table_names:
        delete_CustomTable(conn, table_name)


def create_SubjectsTable(conn):
    cursor = conn.cursor()
    cursor.execute(
        '''
        create table if not exists subjects (
            subject text
        )
        '''
    )
    conn.commit()
    conn.close()


def AddToSubjectsTable(conn, subject):
    cursor = conn.cursor()
    cursor.execute(
        '''
        insert into subjects (subject) values (?)
        ''', (subject,)
    )
    conn.commit()
    conn.close()


def RemoveSubjectsTable(conn, subject):
    conn = sql_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
            delete from subjects where subject = ?
        ''', (subject,)
    )
    conn.commit()
    conn.close()


def load_subjects(conn):
    cursor = conn.cursor()
    cursor.execute(
        '''
        select * from subjects
        '''
    )
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    subjects = []
    for (s,) in rows:
        subjects.append(s)
    return subjects


def fetchUser(conn, userid, password):
    cursor = conn.cursor()
    
    cursor.execute(
        '''
        select userID, password from users
        '''
    )

    rows = cursor.fetchall()
    
    for (user, pw) in rows:
        if (user == userid) and shc.verify(password, pw):
            return True
    return False


def convertToBinaryData(filename):
    # Convert digital data to binary format
    if not filename:
        return ""
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertDataToTable(conn,table_name, *args):
    question_no = args[0]
    question = args[1]
    image = args[2]
    optionA = args[3]
    optionB = args[4]
    optionC = args[5]
    optionD = args[6]
    answer = args[7]

    cursor = conn.cursor()
    cursor.execute(
        f'''
        insert into {table_name} (id, question, image, optionA, optionB, optionC, optionD, answer) 
        values (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (question_no, question, image, optionA, optionB, optionC, optionD, answer,)
    )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    conn = sql_connection()
    #create_UserTable(conn)
    create_SubjectsTable(conn)
    

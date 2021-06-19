import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pandas as pd


database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName('database.db')

if not database.open():
    print("Unable to open database")
    sys.exit(1)

query = QSqlQuery()

# query.exec_(
#     """
#     CREATE TABLE subjects (
#         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         subject VARCHAR(80) NOT NULL,
#         questionRefs VARCHAR(80) NOT NULL
#     )
#     """
# )

# query.exec_(
#     """
#     CREATE TABLE crs_question (
#         question_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL REFERENCES crs_option(option_id),
#         question VARCHAR(1000) NOT NULL,
#         image_file VARCHAR(20) NOT NULL
#     )
#     """
# )

# query.exec_(
#     """
#     CREATE TABLE science_question (
#         question_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL REFERENCES science_option(option_id),
#         question VARCHAR(1000) NOT NULL,
#         image_file VARCHAR(20) NOT NULL
#     )
#     """
# )


# query.exec_(
#     """
#     CREATE TABLE crs_option (
#         option_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         optionA VARCHAR(2) NOT NULL,
#         optionB VARCHAR(2) NOT NULL,
#         optionC VARCHAR(2) NOT NULL,
#         optionD VARCHAR(2) NOT NULL
#     )
#     """
# )

# query.exec_(
#     """
#     CREATE TABLE science_option (
#         option_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         optionA VARCHAR(2) NOT NULL,
#         optionB VARCHAR(2) NOT NULL,
#         optionC VARCHAR(2) NOT NULL,
#         optionD VARCHAR(2) NOT NULL
#     )
#     """
# )



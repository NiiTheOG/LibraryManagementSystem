import sqlite3
connection = sqlite3.connect('Library.db')
cursor = connection.cursor()
cursor.execute("""UPDATE LOAN_RESERVATION_STATUS
                SET Status = 'available'
                WHERE "BOOK ID" = 19 AND "CHECKOUT DATE" = '22/09/2020' """)

records=cursor.fetchall()#or fetchmany(n), fetchone()
print(records)

connection.commit()
connection.close()

"""SELECT [BOOK ID], [TITLE], [GENRE], [AUTHOR], [STATUS] 
            FROM ( 
                SELECT *, 
                RANK () OVER ( 
                    PARTITION BY 'Book ID' 
                    ORDER BY LOAN_RESERVATION_STATUS.'Return Date' 
                ) LengthRank 
            FROM 
                LOAN_RESERVATION_STATUS, BOOK_INFO 
            WHERE LOAN_RESERVATION_STATUS.'Book ID' = BOOK_INFO.ID 
            AND TITLE LIKE 'GREAT BY CHOICE'
            ) 
            WHERE LengthRank  = 1;"""

# def InsertSQLStatement(title, author, price, genre):
#     flag = True
#     try:
#         sqliteConnection = sqlite3.connect('Library.db')
#         cursor = sqliteConnection.cursor()

#         sqlite_insert_query = """ INSERT INTO RecommendedBooks
#                                             (Title, Author, Price, Genre) 
#                                             VALUES (?, ?, ?, ?)"""
        
#         data_tuple = (title, author, price, genre)
        
#         cursor.execute(sqlite_insert_query, data_tuple)
#         sqliteConnection.commit()
#         print("Record added to DB")

#         sqliteConnection.close()
#     except sqlite3.Error as error:
#         flag = False
#         print("Failed to insert record into table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("the sqlite connection is closed")
#     return flag

# r = open('newRecbooklist.txt', 'r')
# next(r)
# for line in r:
#     records = line.strip()
#     records = records.split(',')
#     InsertSQLStatement(records[1], records[2], records[3], records[4])


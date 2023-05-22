# COP501 CW
# Database Layer
# By F219655
'''
All functions required for database operations.
To use: Create an instance of Database class to access related functions.
'''
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import pickle

class Book(object):
    '''Class for Book items'''
    def __init__(self, id, genre, title, author, purchase_price, purchase_date):
        '''Constructor'''
        self.id = id
        self.genre = genre
        self.title = title
        self.author = author
        self.price = purchase_price
        self.date = purchase_date

class Database(object):
    '''Class for Database connection and other related functions'''
    def __init__(self):
        '''Constructor'''
        self.database = 'Library.db'
        self.populateDB()
    

    def InsertSQLStatement(self,sqlite_insert_query, data_tuple):
        '''Function for inserting records into database
            sqlite_insert_query: string
            data_tuple: tuple
            Returns
            flag: True if records are added and False if not added
        '''
        flag = True
        try:
            sqliteConnection = sqlite3.connect(self.database)
            cursor = sqliteConnection.cursor()
            
            cursor.execute(sqlite_insert_query, data_tuple)
            sqliteConnection.commit()
            print("Record added to DB")

            sqliteConnection.close()
        except sqlite3.Error as error:
            flag = False
            print("Failed to insert record into table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("the sqlite connection is closed")
        return flag

    def insertBook(self, book_object):
        '''This function inserts book records into the database
            book_object: A Book object
        '''
        sqlite_insert_query = """ INSERT INTO Book_Info
                                                (ID, Genre, Title, Author, [Purchase Price £], [Purchase Date]) 
                                                VALUES (?, ?, ?, ?, ?, ?)"""
        data_tuple = (book_object.id, book_object.genre, book_object.title, book_object.author, 
                        book_object.price, book_object.date)
        self.InsertSQLStatement(sqlite_insert_query, data_tuple)

    def insertLoanHist(self, book_id, reserve_date, checkout_date, return_date, member_id):
        '''This function inserts loan and reservation history into the database
            records into it 
            book_id:int
            reserve_date: string
            checkout_date: string
            return_date: string
            member_id:int
        '''
        sqlite_insert_query = """ INSERT INTO Loan_Reservation_History
                                                ([Book ID], [Reservation Date], [Checkout Date], [Return Date], [Member ID]) 
                                                VALUES (?, ?, ?, ?, ?)"""
        data_tuple = (book_id, reserve_date, checkout_date, return_date, member_id)
        self.InsertSQLStatement(sqlite_insert_query, data_tuple)
    
    def insertLoanHistStatus(self):
        '''This function inserts the transaction log into another table and
            creates a new column to indicate availability
        '''
        sqlite_insert_query = """INSERT INTO Loan_Reservation_Status
                                SELECT 
                                Loan_Reservation_History."Book ID",
                                Loan_Reservation_History."Reservation Date",
                                Loan_Reservation_History."Checkout Date",
                                Loan_Reservation_History."Return Date",
                                Loan_Reservation_History."Member ID",
                                case when Loan_Reservation_History."Checkout Date" = '-' 
                                    and Loan_Reservation_History."Return Date" = '-' then 'reserved'
                                when Loan_Reservation_History."Return Date" = '-' then 'loan'
                                else 'available'
                                end Status
                            from Loan_Reservation_History left join Loan_Reservation_Status
                            on (Loan_Reservation_History."Book ID",
                            Loan_Reservation_History."Reservation Date", 
                            Loan_Reservation_History."Checkout Date", 
                            Loan_Reservation_History."Member ID") = 
                            (Loan_Reservation_Status."Book ID", 
                            Loan_Reservation_Status."Reservation Date", 
                            Loan_Reservation_Status."Checkout Date", 
                            Loan_Reservation_Status."Member ID")
                        """
        data_tuple = ()
        self.InsertSQLStatement(sqlite_insert_query, data_tuple)

    def readBookInfo(self):
        '''This function reads book records from the Book_Info file
            into the database
        '''
        f = open('Book_Info.txt', 'r')

        for line in f:
            bookinfo = line.strip()
            bookinfo = bookinfo.split(',')
            book = Book(bookinfo[0], bookinfo[1], bookinfo[2], bookinfo[3], bookinfo[4], bookinfo[5])
            self.insertBook(book)
        
    def readLoanHist(self):
        '''This function reads loan reservation history records from the 
            Loan_Reservation_History file into the database
        '''
        l = open('Loan_Reservation_History.txt', 'r')
        next(l)
        for line in l:
            records = line.strip()
            records = records.split(',')
            self.insertLoanHist(records[0], records[1], records[2], records[3], records[4])
    
    def CheckBookInfo(self):
        '''This function checks if the Book_Info table is empty
            Returns: a list item indicating 1 if empty
        '''
        res = self.RunSQLStatement("""SELECT CASE WHEN EXISTS(SELECT 1 FROM Book_Info) THEN 0
                                        ELSE 1 END AS IsEmpty""")
        return res
    
    def CheckLoanHist(self):
        '''This function checks if the Loan_Reservation_History table is empty
            Returns: a list item indicating 1 if empty
        '''
        res = self.RunSQLStatement("""SELECT CASE WHEN EXISTS(SELECT 1 FROM Loan_Reservation_History) THEN 0
                                     ELSE 1 END AS IsEmpty""")
        return res
    
    def CheckLoanHistStatus(self):
        '''This function checks if the Loan_Reservation_Status table is empty
            Returns: a list item indicating 1 if empty
        '''
        res = self.RunSQLStatement("""SELECT CASE WHEN EXISTS(SELECT 1 FROM Loan_Reservation_Status) THEN 0
                                     ELSE 1 END AS IsEmpty""")
        return res

    def populateDB(self):
        '''This function populates the database with data from the files'''
        checkbooktable = self.CheckBookInfo()
        checkhisttable = self.CheckLoanHist()
        checkloanstatus = self.CheckLoanHistStatus()

        booktable_isEmpty = checkbooktable[0]['IsEmpty']
        loanhist_isEmpty = checkhisttable[0]['IsEmpty']
        loanstatus_isEmpty = checkloanstatus[0]['IsEmpty']

        if booktable_isEmpty == 1:
            self.readBookInfo()
        
        if loanhist_isEmpty == 1:
            self.readLoanHist()

        if loanstatus_isEmpty == 1:
            self.insertLoanHistStatus()

    def RunSQLStatement(self, SQLStatement):
        '''Function to run sql statements
            SQLStatement: string
            Returns
            result: dictionary with database records
        '''
        try:
            sqliteConnection = sqlite3.connect(self.database)
            df=pd.read_sql(SQLStatement,sqliteConnection)
            result = df.to_dict('records')
            
        except sqlite3.Error as error:
            print()
            result="some error:"+ str(error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("the sqlite connection is closed")    

        return result

    def searchBookByTitle(self, book):
        '''Function to search for book by title
            book: string
            Returns
            result: dictionary of books with given title
        '''
        result = self.RunSQLStatement(
            """SELECT * FROM(
                SELECT "BOOK ID", "TITLE", "GENRE", "AUTHOR", "STATUS"
                FROM (
                    SELECT
                    *,
                    RANK () OVER ( 
                        PARTITION BY "Book ID"
                        ORDER BY LOAN_RESERVATION_STATUS."Return Date"
                    ) LengthRank 
                FROM LOAN_RESERVATION_STATUS, BOOK_INFO
                WHERE LOAN_RESERVATION_STATUS."Book ID" = BOOK_INFO.ID
                AND TITLE LIKE '%{}%'
                )  
                WHERE LENGTHRANK  = 1)
                WHERE STATUS = 'available'
            UNION
                SELECT "BOOK ID", "TITLE", "GENRE", "AUTHOR", "STATUS"
                FROM (
                    SELECT
                    *,
                    RANK () OVER ( 
                        PARTITION BY "Book ID"
                        ORDER BY LOAN_RESERVATION_STATUS."Return Date"
                    ) LengthRank 
                FROM LOAN_RESERVATION_STATUS, BOOK_INFO
                WHERE LOAN_RESERVATION_STATUS."Book ID" = BOOK_INFO.ID
                AND TITLE LIKE '%{}%'
                )  
                WHERE LENGTHRANK  = 1;""".format(book, book)
            )   
        return result

    def reservebook(self,bookid, reservationdate, memberid):
        '''Function to reserve books
            bookid: int
            reservationdate: string
            memberid: string
            Returns
            result: True if record is added and False if not added
        '''
        sqlite_insert_query = """ INSERT INTO LOAN_RESERVATION_STATUS
                                    VALUES (?,?,?,?,?,?)"""
        data_tuple = (bookid, reservationdate, '-', '-', memberid, 'reserved')
        result = self.InsertSQLStatement(sqlite_insert_query, data_tuple)
        return result

    def checkoutbook(self, bookid, checkoutdate, memberid):
        '''Function to checkout books
            bookid: int
            checkoutdate: string
            memberid: string
            Returns
            result: True if record is added and False if not added
        '''
        sqlite_insert_query = """ INSERT INTO LOAN_RESERVATION_STATUS
                                    VALUES (?,?,?,?,?,?)"""
        data_tuple = (bookid, '-', checkoutdate, '-', memberid, 'loan')
        result = self.InsertSQLStatement(sqlite_insert_query, data_tuple)
        return result

    def checkBookID(self,id):
        '''Function to validate bookid
            id: int
            Returns
            result: dictionary oof books with given id
        '''
        result = self.RunSQLStatement(
            """SELECT "BOOK ID", "TITLE", "GENRE", "AUTHOR", "STATUS", "CHECKOUT DATE"
                FROM (
                    SELECT
                    *,
                    RANK () OVER ( 
                        PARTITION BY "Book ID"
                        ORDER BY LOAN_RESERVATION_STATUS."Return Date"
                    ) LengthRank 
                FROM LOAN_RESERVATION_STATUS, BOOK_INFO
                WHERE LOAN_RESERVATION_STATUS."Book ID" = BOOK_INFO.ID
                AND "BOOK ID" = {}
                )  
                WHERE LENGTHRANK  = 1
            """.format(id)
        )
        return result

    def updateBookReturn(self, id, status, checkoutdate, returndate):
        '''Function to update book record from loan status to available when returned
            id: int
            status: string
            checkoutdate: string
            returndate: string
            Returns
            result: True if record is added and False if not added
        '''
        result = self.InsertSQLStatement("""UPDATE LOAN_RESERVATION_STATUS
                    SET Status = ?,
                    "RETURN DATE" = ?
                    WHERE "BOOK ID" = ? AND "CHECKOUT DATE" = ? """, (status, returndate, id, checkoutdate))
        return result
    
    def updateReserveReturn(self, id, status, checkoutdate, returndate):
        '''Function to update book record for a book that has been reserved.
            The new status is set to loan with the assumption that the member who reserved checks
            out the book the day the book is returned
            id: int
            status: string
            checkoutdate: string
            returndate: string
            Returns
            result: True if record is added and False if not added
        '''
        result = self.InsertSQLStatement("""UPDATE LOAN_RESERVATION_STATUS
                    SET Status = ?,
                    "CHECKOUT DATE" = ?
                    WHERE "BOOK ID" = ? AND "CHECKOUT DATE" = ? """, (status, returndate, id, checkoutdate))
        return result
    

    def selectrecommendedbooksdf(self):
        '''Function to get books used for recommendation from database.
            It has its own connection to the database because we want a pandas dataframe returned
            Returns
            result: a dataframe with books used for recommendation
        '''
        try:
            SQLStatement = """SELECT * FROM RECOMMENDEDBOOKS"""
            sqliteConnection = sqlite3.connect(self.database)
            df=pd.read_sql(SQLStatement,sqliteConnection)
            result = df
            
        except sqlite3.Error as error:
            print()
            result="some error:"+ str(error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("the sqlite connection is closed")    

        return result

    def selectmostpopularbk(self):
        '''Function to get mostpopular book from database
            Returns
            result: dictionary with most popular book record
        '''
        result = self.RunSQLStatement("""SELECT "TITLE", Author, "Purchase Price £", Genre, COUNT(*)
                    FROM LOAN_RESERVATION_STATUS INNER JOIN BOOK_INFO
                    ON LOAN_RESERVATION_STATUS."Book ID" = BOOK_INFO.ID
                    GROUP BY 1
                    ORDER BY 5 DESC
                    LIMIT 1
        """)

        return result

    def selectbookhistory(self):
        '''Function to get log count of books in database
            Returns
            result: dictionary with log count of books
        '''
        result = self.RunSQLStatement("""SELECT "TITLE", Author, "Purchase Price £", Genre, COUNT(*)
                        FROM LOAN_RESERVATION_STATUS INNER JOIN BOOK_INFO
                        ON LOAN_RESERVATION_STATUS."Book ID" = BOOK_INFO.ID
                        GROUP BY 1
                        ORDER BY 5 DESC
        """)

        return result

    def selectmostrequestedbook(self):
        '''Function to get breakdown of most popular book stats into Reserved, Loan and Returned
            Returns
            result: dictionary with count of most popular book stats based on categories
             (Reserved, Loan and Returned)
        '''
        result = self.RunSQLStatement("""SELECT "TITLE", Author, Status, Genre, COUNT(*)
                FROM LOAN_RESERVATION_STATUS INNER JOIN BOOK_INFO
                ON LOAN_RESERVATION_STATUS."Book ID" = BOOK_INFO.ID
                WHERE TITLE like (SELECT TITLE FROM
                                    (SELECT "TITLE", Author, "Purchase Price £", Genre, COUNT(*)
                            FROM LOAN_RESERVATION_STATUS INNER JOIN BOOK_INFO
                            ON LOAN_RESERVATION_STATUS."Book ID" = BOOK_INFO.ID
                            GROUP BY 1
                            ORDER BY 5 DESC
                            LIMIT 1))
                GROUP BY 1,3
                ORDER BY 1 DESC;
        """)
        return result
    
    def getbookcover(self,id):
        '''This function gets the image associated with the id of a given book
            id: int
            Returns: an array representation of the image
        '''
        try:
            sqliteConnection = sqlite3.connect(self.database)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sql_fetch_blob_query = """Select Book_Info.ID, photo
                        from Book_Info inner join BookInventory
                        on Book_Info.Title = BookInventory.Title
                        where Book_Info.ID = ?"""
            cursor.execute(sql_fetch_blob_query, (id,))
            record = cursor.fetchall()
            for row in record:
                print("Id = ", row[0])
                photo = pickle.loads(row[1]) #unpacking photo to array
                return photo
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read blob data from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("sqlite connection is closed")
    
    def reset(self):
        '''This function resets the database and populates it again'''
        flag = True
        data_tuple = ()
        loanhiststatusreset = self.InsertSQLStatement("DELETE FROM Loan_Reservation_Status", data_tuple)
        loanhistreset = self.InsertSQLStatement("DELETE FROM Loan_Reservation_History", data_tuple)
        bookinforeset = self.InsertSQLStatement("DELETE FROM Book_Info", data_tuple)
        if loanhiststatusreset and loanhistreset and bookinforeset:
            self.populateDB()
            return flag


def main():
    ###### testing ######
    db = Database()
    runsql = db.RunSQLStatement('Select * from Book_Info')
    print('------Book Info Test------')
    print(runsql)

    idcheck = db.checkBookID(45)
    print('------Book ID Check------')
    print(idcheck)

if __name__ =='__main__':
    print(main())

# COP501 CW
# Control Layer(BookSearch Module)
# By F219655
'''
All functions required for searching for a book based on title.
To use: Import the bookSearch module to access related functions.
'''
import database

db = database.Database()

def bookSearch(searchterm):
    '''This function searches for books in the database using their titles
        searchterm: string (Title of the book)
        Returns 
        result: a list of books with given title
    '''
    # remove extra characters from input string
    booktitle = searchterm.strip()
    result = db.searchBookByTitle(booktitle)

    return result

def main():
    ###### testing ######
    # search for a book with any characters in book title
    searchresults = bookSearch('rog')
    print(searchresults)

if __name__ =='__main__':
    print(main())
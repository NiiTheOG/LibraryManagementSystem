# COP501 CW
# Control Layer(BookReturn Module)
# By F219655
'''
All functions required for returning books using the ID.
To use: Import the module bookReturn to access related functions.
'''
import database
from datetime import date

# get todays date
today = date.today()

# create database object
db = database.Database()

todaysdate = today.strftime("%d/%m/%Y")

def bookReturn(id):
    '''This function checks if a book id is valid or its status
        id: int (Book ID)
        Returns
        returnmsg: the status of the book return request
    '''
    # get book from database using id 
    result = db.checkBookID(id)

    # check if book id is valid using the length of result
    if len(result) == 0:
        returnmsg = "Invalid Book ID. Retry"

    # if book is available in database, then it cannot be returned
    elif result[-1]['Status'] == 'available':
        returnmsg = "The ID you have entered is for a book that is already available"
    
    # if book has been reserved by another person the book status is updated
    # the previous loan status of the book is updated to available 
    # but it is assumed that the person who made the reservation comes for the book on the same day
    # so the reservation status is also changed to loan
    # The latest status of the book that will be displayed is loan because of this assumption
    elif result[-1]['Status'] == 'reserved':
        upd = db.updateBookReturn(id, 'available', result[-2]["Checkout Date"], todaysdate)
        upd2 = db.updateReserveReturn(id, 'loan', result[-1]["Checkout Date"], todaysdate)
        if upd and upd2:
            returnmsg = "Thank you for returning the book. It has been reserved by another member"
        else: 
            returnmsg = "Book could not be returned"
    # if the book is on loan and has not been reserved by anyone checkout successfully
    elif result[-1]['Status'] == 'loan':
        upd = db.updateBookReturn(id, 'available', result[-1]["Checkout Date"], todaysdate)
        if upd:
            returnmsg = "Thank you for returning the book!"
        else:
            returnmsg = "Book could not be returned"
    
    return returnmsg

def main():
    ###### testing ######
    # Case 1: Invalid Book ID
    case1 = bookReturn(66)
    print('Case 1:',case1)

    # Case 2: Trying to return a book that is already available
    case2 = bookReturn(50)
    print('Case 2:', case2)

    # Case 3: Returning a book that is reserved by another member
    case3 = bookReturn(11)
    print('Case 3:', case3)

if __name__ =='__main__':
    print(main())


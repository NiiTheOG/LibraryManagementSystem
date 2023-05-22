# COP501 CW
# Control Layer(BookCheckout Module)
# By F219655
'''
All functions required for checking out books.
To use: Import the bookCheckout module to access related functions.
'''
import database
import re
from datetime import date
import matplotlib.pyplot as plt

# get todays date
today = date.today()
# create database object
db = database.Database()

#reformat date string
todaysdate = today.strftime("%d/%m/%Y")

def regexcheck(memberid):
    '''This function validates the member id
        memberid: int
        Returns 
        reg: a match object if id is a 4 digit number else None
    '''
    # define regular expression
    regex= "\d{4}"
    
    # match with member id
    idcheck = re.compile(regex)
    reg = idcheck.match(str(memberid))

    return reg

def bookCheckout(bookid,memberid,flag):
    '''This function is the first option for book checkouts.
        It is used to check out books that have been searched for.
        bookid: int
        memberid: int
        flag: string (The flag indicates the status of a book 'r'-Reserved 'l'-Loan)
        Returns
        status: The response message for a bookcheckout request
    '''
    # check member id
    check = regexcheck(memberid)
   
    if check is not None:
        # if book is on loan, reserve book
        if flag == 'l':
            result = db.reservebook(bookid, todaysdate, memberid)
            if result:
                status = 'Book has been reserved successfully!'
            else:
                status = 'Book could not be reserved. Retry'
        
        # if book has been reserved, allow for another reservation
        elif flag == 'r':
            result = db.reservebook(bookid, todaysdate, memberid)
            if result:
                status = 'Book has been reserved successfully!'
            else:
                status = 'Book could not be reserved. Retry'
        
        # if book is available, check out successfully
        else:
            result = db.checkoutbook(bookid, todaysdate, memberid)
            if result:
                status = 'Book has been checked out successfully!'
            else:
                status = 'Book could not be checked out. Retry'
    else:
        status = 'Invalid Member ID'

    return status

def checkout(id, memberid):
    '''This function is the second option for book checkouts.
        It is used to check out books manually without searching for them.
        id: int (Book ID)
        memberid: int
        Returns
        status: The response message for a bookcheckout request
    '''
    # validate book id
    result = db.checkBookID(id)
    # validate member id
    check = regexcheck(memberid)

    if result and check:
        # if book is on loan or reserved return reservation option
        if (result[-1]['Status'] == 'reserved') or (result[-1]['Status'] == 'loan'):
            status = "Book is on loan. Would you like to reserve?"
        
        # if book is available, checkout successfully
        else:
            result = db.checkoutbook(id, todaysdate, memberid)
            if result:
                status = "Book Checked out successfully!"
            else:
                status = "Book could not be checked out. Retry"
    else:
        status = "Invalid Book or Member ID"

    return status

def reservebk(id, memberid):
    '''This function reserves a book if the user agrees with reservation option
        id: int
        memberid: int
        Returns
        status: The response message for a bookcheckout request
    '''
    db.reservebook(id,todaysdate,memberid)
    status = "Book reserved sucessfully!"
    return status

def getbookimage(id):
    '''This function gets the cover of the book using the id
        id: int
    '''
    fig = plt.figure(figsize=(2,2), facecolor="#e4e4e4") 
    ax = fig.add_subplot(1,1,1)
    img = db.getbookcover(id)
    ax.imshow(img)
    plt.grid(False)
    plt.axis('off')
    return fig

def main():
    ###### testing ######
    
    # Checkout after search(bookid is passed from search page)
    # Case 1: Invalid Member ID
    case1 = bookCheckout(2, 'g4g7', 'r')
    print('Case 1:',case1)
    # Case 2: Reservation Successful 
    case2 = bookCheckout(19, '8888', 'l')
    print('Case 2:',case2)

    # Manual Checkout (Checking out by entering both book and member id )
    # Case 3: Invalid Book ID
    case3 = checkout(58, '5677')
    print('Case 3:',case3)


if __name__ =='__main__':
    print(main())
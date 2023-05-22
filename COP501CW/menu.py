# COP501 CW
# View Layer(Menu Module)
# By F219655
'''
Menu options for program functionalities.
To use: Create a tkinter window instance and pass it to an instance of the MainGUI class
'''
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import bookSearch as bs
import bookCheckout as bc
import bookReturn as br
import bookSelect as bslct


class MainGUI:
    '''Class for Menu options'''
    def __init__(self, window):
        '''Constructor
            window: tkinter window
        '''
        self.__win = window
        self.__win.title("Library Management System")
        self.__win.geometry("950x750")
        self.__win.resizable(False, False)
        self.__bg = PhotoImage(file="background.png")
        self.__lfont = ("Helvetica", 30, 'normal')
        self.__bfont = ("Helvetica", 15, 'normal')
        self.__winbg = Label(self.__win, image=self.__bg)
        self.__winbg.place(x=0, y=0,relwidth=1, relheight=1)
        self.__tabControl = Notebook(self.__win)
        self.__tab1 = Frame(self.__tabControl) 
        self.__tab2 = Frame(self.__tabControl)
        self.__tab3 = Frame(self.__tabControl)
        self.__tab4 = Frame(self.__tabControl)
        self.__tab5 = Frame(self.__tabControl)
        self.__frame1 = Frame(self.__tab1, width=900, height=700)
        self.__frame2 = Frame(self.__tab2, width=900, height=700)
        self.__frame3 = Frame(self.__tab3, width=900, height=700)
        self.__frame4 = Frame(self.__tab4, width=900, height=700)
        self.__frame5 = Frame(self.__tab5, width=900, height=700)
        self.__frame = Frame(self.__frame1)
        self.__recframe = Frame(self.__frame4)
        self.__bkstatus = Label(self.__frame3, text="")
        
        
        self.__tabControl.add(self.__tab1, text='Home')
        self.__tabControl.add(self.__tab2, text='Checkout')
        self.__tabControl.add(self.__tab3, text='Return Book')
        self.__tabControl.add(self.__tab4, text='Recommend')
        self.__tabControl.add(self.__tab5, text='Reset')  
        self.__tabControl.grid(row=0,column=3,rowspan=10)
        self.__frame1.grid(row=0,column=0, rowspan=10)
        self.__frame2.grid(row=0,column=0, rowspan=10)
        self.__frame3.grid(row=0,column=0, rowspan=10)
        self.__frame4.grid(row=0,column=0, rowspan=10)
        self.__frame5.grid(row=0,column=0, rowspan=10)
        self.__frame.grid(row=3, column=1)
        self.__recframe.grid(row=3, column=1)

        self.__createSearchpage()
        self.__createBookReturnPage()
        self.__createGraphs()
        self.___createCheckoutpage()
        self.__createResetpage()
    
    def __createSearchpage(self):
        '''Creates Search page'''
        header = Label(self.__frame1, 
                            text="Welcome to the Library Management System",
                            foreground = "purple",
                            font=self.__lfont)
        header.grid(row=1, column=1)
        bklabel = Label(self.__frame1, text="Book Title:")
        bklabel.grid(row=2, column=0)
        bookname = StringVar(self.__frame1)
        self.__bksearch = Entry(self.__frame1, textvariable=bookname)
        self.__bksearch.bind("<KeyPress>", self.__ShowBooks)
        # searchbtn = Button(self.__frame1, text='Search', state='normal', command=self.__ShowBooks)
        self.__bksearch.grid(row=2, column=1)
        # searchbtn.grid(row=2, column=2)

    
    def __updateframe(self,frame):
        '''Function to update a frame on window
            frame: frame to update
        '''
        for widgets in frame.winfo_children():
            widgets.destroy()
    
    def __ShowBooks(self, bookname):
        '''Function to search for book with book title'''
        self.__updateframe(self.__frame)
        
        results = bs.bookSearch(self.__bksearch.get())
        
        header=Label(self.__frame,width=10,text='Book ID',borderwidth=2, font=self.__bfont, 
                    relief='ridge',anchor='center',foreground = "purple")
        header.grid(row=0,column=0)
        header=Label(self.__frame,width=20,text='Title',borderwidth=2, font=self.__bfont,
                    relief='ridge',anchor='center', foreground = "purple",)
        header.grid(row=0,column=1)
        header=Label(self.__frame,width=20,text='Genre',borderwidth=2, font=self.__bfont,
                    relief='ridge',anchor='center', foreground = "purple")
        header.grid(row=0,column=2)
        header=Label(self.__frame,width=15,text='Author',borderwidth=2, font=self.__bfont,
                    relief='ridge',anchor='center', foreground = "purple")
        header.grid(row=0,column=3)
        header=Label(self.__frame,width=10,text='Availability',borderwidth=2, font=self.__bfont,
                    relief='ridge',anchor='center', foreground = "purple")
        header.grid(row=0,column=4)

        i = 1
        for book in results:
            bookid = Label(self.__frame, text=book['BOOK ID'], width=10, font=self.__bfont,
                        relief='ridge',anchor='center', foreground = "#121619")
            bookid.grid(row=i,column=0)
            title = Label(self.__frame,text=book['TITLE'], width=20, font=self.__bfont,
                        relief='ridge',anchor='center', foreground = "#121619")
            title.grid(row=i, column=1)
            genre = Label(self.__frame,text=book['GENRE'], width=20, font=self.__bfont,
                        relief='ridge',anchor='center')
            genre.grid(row=i, column=2)
            author = Label(self.__frame, text=book['AUTHOR'], width=15, font=self.__bfont,
                        relief='ridge',anchor='center')
            author.grid(row=i, column=3)
            status = Label(self.__frame, text=book['STATUS'], width=10, font=self.__bfont,
                        relief='ridge',anchor='center')
            status.grid(row=i, column=4)
            checkout = Button(self.__frame,text='Reserve' if book['STATUS'] == 'loan' else 'Check Out', 
                                state = "disabled" if book['STATUS'] == 'reserved' else "normal", 
                                command=lambda s=book['STATUS'],id=book['BOOK ID']: self.__ShowCheckoutTab(id,s))
            checkout.grid(row=i, column=6)
            i = i + 1
    
    def ___createCheckoutpage(self):
        '''Creates Page for Manual Checkouts.ie.using both book and member id'''
        header = Label(self.__frame2, 
                    text="Welcome to the Book Checkout page",
                    foreground="purple",
                    font=self.__lfont)
        header.grid(row = 0, column=1)
        bklabel = Label(self.__frame2, text="Book ID:")
        bklabel.grid(row=1, column=0)
        bookid = StringVar(self.__frame2)
        self.bookidentry = Entry(self.__frame2, textvariable=bookid)
        self.bookidentry.grid(row=1, column=1)
        
        mlabel = Label(self.__frame2, text="Member ID:")
        mlabel.grid(row=2, column = 0)
        memberid = StringVar(self.__frame2)
        self.memberidentry = Entry(self.__frame2, textvariable=memberid)
        self.memberidentry.grid(row=2, column=1)

        submit = Button(self.__frame2, text="Submit", 
                        command=lambda : self.__manualCheckOut(self.bookidentry.get(),self.memberidentry.get()))
        submit.grid(row=3, column=1)
    
    def __ShowCheckoutTab(self,bookid, status):
        '''Creates Page for Book checkout when book has been searched for
            bookid: int
            status: string
        '''
        self.__updateframe(self.__frame2)
        self.__tabControl.select(self.__tab2)

        if status == 'reserved':
            flag = 'r'
        elif status == 'loan':
            flag = 'l'
        else:
            flag = 'a'
        title = Label(self.__frame2, 
                    text='Reserve book with id %d'%(bookid) 
                    if status == 'loan' else 'Check out book with id %d'%(bookid), 
                    font=self.__lfont, anchor='center',
                    foreground="purple")
        title.grid(row=1,column=0)
        bkimg = bc.getbookimage(bookid)
        canvas = FigureCanvasTkAgg(bkimg, master=self.__frame2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)
        mIdlabel = Label(self.__frame2, text='Member ID:')
        mIdlabel.grid(row=3, column=0)
        mId = StringVar(self.__frame2)
        self.memberid = Entry(self.__frame2, textvariable=mId)
        self.memberid.grid(row=3, column=1)
        submit = Button(self.__frame2, 
                        text="Reserve" if status == 'loan' else "Check Out",
                        command=lambda b=bookid: self.__checkout(b,self.memberid.get(),flag))
        submit.grid(row=3, column=2)
    
    def __checkout(self,bookid, memberid, flag):
        '''Function to checkout book that has been searched for
            bookid: int
            memberid: int
            flag: string (indicates the status of a book)
        '''
        result = bc.bookCheckout(bookid, memberid, flag)

        resp1 = 'Invalid Member ID'

        if result == resp1:
            inv = Label(self.__frame2, text=result, foreground='red')
            inv.grid(row=4, column=1)
        else:
            inv = Label(self.__frame2, text=result, foreground='green')
            inv.grid(row=4, column=1)
        self.memberid.delete(0, 'end')
        
    
    def __manualCheckOut(self, bookid, memberid):
        '''Function to check out book without searching
            bookid: int
            memberid: int
        '''
        result = bc.checkout(bookid, memberid)

        resp = 'Book is on loan. Would you like to reserve?'
        resp1 = 'Invalid Book or Member ID'
        
        if result == resp:
            self.__reservationoption(bookid, memberid)
        elif result == resp1:
            status = Label(self.__frame2, text=result, foreground="red")
            status.grid(row=4, column=1)
        else:
            status = Label(self.__frame2, text=result, foreground="green")
            status.grid(row=4, column=1)
        self.memberidentry.delete(0, "end")
        self.bookidentry.delete(0,"end")
    
    def __reservationoption(self, bookid, memberid):
        '''Function to show book reservation option
            bookid: int
            memberid: int
        '''
        frameR = Frame(self.__frame2)
        frameR.grid(row=5, column=1)

        reservelabel = Label(frameR, text="Book on Loan. Proceed to Reserve:", 
                            font=self.__bfont, foreground="purple")
        reservelabel.grid(row=5, column=0)
        yesbtn = Button(frameR, text="Confirm", command=lambda b=bookid, m=memberid:self.__reservebk(b,m))
        yesbtn.grid(row=5, column=1)
        nobtn = Button(frameR, text="Decline", command=lambda f=frameR:self.__updateframe(f))
        nobtn.grid(row=5, column=2)
    
    def __reservebk(self, bookid, memberid):
        '''Function to proceed with reservation option
            bookid: int
            memberid: int
        '''
        result = bc.reservebk(bookid, memberid)
        resplbl = Label(self.__frame2, text=result, foreground="green")
        resplbl.grid(row=6, column=1)
    
    def __createBookReturnPage(self):
        '''Creates page for Book Returns'''
        returntitle = Label(self.__frame3, 
                    text="Welcome to the Return Book Page",
                    font=self.__lfont,
                    foreground="purple")
        returntitle.grid(row=0, column=1)
        bklabel = Label(self.__frame3, text="Book ID:")
        bklabel.grid(row=2, column=0)
        bookid = StringVar(self.__frame3)
        self.returnbookid = Entry(self.__frame3, textvariable=bookid)
        self.returnbookid.grid(row=2, column=1)
        
        returnbtn = Button(self.__frame3, 
                            text="Return", 
                            command=lambda : self.__returnStatus(self.returnbookid.get()))
        
        returnbtn.grid(row=2, column=2)


    def __returnStatus(self, id):
        '''Function to return book and display status
            id: int (Book id)
        '''
        result = br.bookReturn(id)
        
        self.__bkstatus.grid_forget()

        resp1 = 'Invalid Book ID. Retry'
        resp2 = 'The ID you have entered is for a book that is already available'
        resp3 = 'Book could not be returned'
        if (result == resp1) or (result == resp2) or (result == resp3):
            self.__bkstatus = Label(self.__frame3, text=result, foreground='red')
            self.__bkstatus.grid(row=3, column=1)
        else:
            self.__bkstatus = Label(self.__frame3, text=result, foreground='green')
            self.__bkstatus.grid(row=3, column=1)
        self.returnbookid.delete(0,"end")
        
    
    def __showBookRecs(self, amt):
        '''Shows book recommendations in a tabular form
            amt: int (Budget)
        '''
        self.__updateframe(self.__recframe)

        recs = bslct.budgetcheck(amt)

        header=Label(self.__recframe,width=30,text='Title',borderwidth=2, font=self.__bfont, 
                    relief='ridge',anchor='center',foreground = "purple")
        header.grid(row=3,column=0)
        header=Label(self.__recframe,width=20,text='Price(£)',borderwidth=2, font=self.__bfont,
                    relief='ridge',anchor='center', foreground = "purple",)
        header.grid(row=3,column=1)
        header=Label(self.__recframe,width=20,text='Genre',borderwidth=2, font=self.__bfont,
                    relief='ridge',anchor='center', foreground = "purple")
        header.grid(row=3,column=2)

        i = 4
        for book in recs:
            title = Label(self.__recframe, text=book['Title'], width=30, font=self.__bfont,
                        relief='ridge',anchor='center', foreground = "#121619")
            title.grid(row=i,column=0)
            price = Label(self.__recframe,text=book['Price'], width=20, font=self.__bfont,
                        relief='ridge',anchor='center', foreground = "#121619")
            price.grid(row=i, column=1)
            genre = Label(self.__recframe,text=book['Genre'], width=20, font=self.__bfont,
                        relief='ridge',anchor='center')
            genre.grid(row=i, column=2)
            i = i + 1
        
    def __createGraphs(self):
        '''Function to display graphs'''
        pagetitle = Label(self.__frame4, 
                        text='Book Stats and Recommendation',
                        font=self.__lfont,
                        foreground="purple")
        pagetitle.grid(row=0,column=1)
        budgetlabel = Label(self.__frame4, text="Budget:")
        budgetlabel.grid(row=1, column=0)
        budget = StringVar(self.__frame4)
        budgetentry = Entry(self.__frame4, textvariable=budget)
        budgetentry.grid(row=1, column=1)
        submitbtn = Button(self.__frame4, 
                            text="Submit",
                            command= lambda : self.__showBookRecs(budget.get()))
        
        submitbtn.grid(row=1, column=2)

        fig = bslct.createGraphs()
        
        canvas = FigureCanvasTkAgg(fig, master=self.__frame4)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, column=1)

    def __createResetpage(self):
        '''Function to create reset database page'''
        pagetitle = Label(self.__frame5,
                            text = 'Reset Database',
                            font=self.__lfont,
                            foreground='purple')
        pagetitle.grid(row=0, column=1)
        resetbtn = Button(self.__frame5, 
                        text = 'Reset',
                        command = self.__reset)
        resetbtn.grid(row=1, column=1)

    def __reset(self):
        '''Calls reset function'''
        result = bslct.reset()
        resp = "Reset successful"

        if result == resp:
            respmsg = Label(self.__frame5, text=result, foreground='green')
            respmsg.grid(row=2, column=1)
        else:
            respmsg = Label(self.__frame5, text=result, foreground='red')
            respmsg.grid(row=2, column=1)


def main():
    window = Tk()
    mGUI=MainGUI(window)
    window.mainloop()

if __name__=='__main__':
	main()

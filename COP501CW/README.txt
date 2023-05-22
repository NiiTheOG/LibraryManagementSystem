##COP501 CW
##By F219655
##Usage

BookSearch: To search for a book, type any set of characters in the book title. The sql query picks the latest record of the book and its availability status

BookCheckout: There are two options. 
1. When the program starts, you can checkout a book directly from the checkout page using book and member id.
2. Search for a book first then checkout based on its availability. The Book Image is displayed with this option.

BookSelect: Book recommendations are done using cosine similarity. The features used are the Book Title, Author and Genre. These features are converted into a weighted matrix then the cosine similarity is calculated. A list of similar books to the most popular book in the library is generated then based on the given budget, the books that fit within the budget are displayed.
Three graphs are displayed to help the librarian decide if it is necessary to purchase new books. The top 5 book titles, top 5 genres and the last graph that shows how often the most popular book is returned, on loan or reserved.

Reset: If a new record is manually added to any of the text files, the reset button should be used to depopulate the database and repopulate it with the new information. Everything is done on the backend.
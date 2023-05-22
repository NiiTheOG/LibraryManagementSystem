# COP501 CW
# Control Layer(BookSelect Module)
# By F219655
'''
All functions required for selecting book for purchase order.
To use: Import the bookSelect module to access related functions.
'''
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import database

# create database object
db = database.Database()

# get table with books for recommendation from database
df = db.selectrecommendedbooksdf()

# get most popular book from database
mostpopularbk = db.selectmostpopularbk()

# define stopwords(words that are not significant for prediction)
N = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 
     'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 
     'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 
     'who', 'ass', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 
     'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 
     'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 
     'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 
     'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 
     'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 
     'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 
     'further', 'was', 'here', 'than', 'the',"it's", 'and', 'it.', 'rt']

# function to remove stopwords
def stopwords_remover(x):
    return [word for word in x if word.lower() not in N]

def recommendationconfig(df):
    '''This function uses the book title, author and genre to recommend similar books to the
        most popular book in the database.
        df: dataframe (The list of books in the database that the recommendations are chosen from)
        Returns
        cosinesim: a sparse matrix with values that represent how similar one book is to the other
        indexes: a list that maps indexes to their titles
    '''
    # create mostpopular book row
    book = {'Title': mostpopularbk[0]['Title'], 'Author': mostpopularbk[0]['Author'], 
            'Price':mostpopularbk[0]['Purchase Price £'], 'Genre':mostpopularbk[0]['Genre']}

    # append most popular book to dataframe with books for recommendation
    df = df.append(book, ignore_index=True)

    # create a new feature for recommendation using title, author and genre
    df['RecFeature'] = df['Title'] + " " + df['Author'] + " " + df['Genre']
    df['RecFeature'] = df['RecFeature'].apply(lambda x : str(x).split())

    # remove stop words
    df['temp'] = df['RecFeature'].apply(lambda x: stopwords_remover(x))
    # put words back together
    df['temp'] = df['temp'].apply(lambda x: " ".join(x) )

    # create a countvectorizer that will transform words into a matrix of counts based on frequency
    countvector = CountVectorizer()
    tokenizedMatrix = countvector.fit_transform(df['temp'])

    # assign weights to these counts using TF-IDF
    tfidf_transformer = TfidfTransformer()
    tfidfMatrix = tfidf_transformer.fit_transform(tokenizedMatrix)

    # compute cosine similarity between books using weighted matrix
    cosinesim = cosine_similarity(tfidfMatrix)
    indexes = pd.Series(df.index, index = df['Title']).drop_duplicates()
    return cosinesim, indexes

def getrecommendedbooks(title, cosinesim, indexes):
    '''This function gets the top 10 similar books to the most popular book
        title: string
        cosinesim: matrix
        indexes: series
        Returns
        a list of most similar books ordered by descending similarity
    '''
    # get index of most popular book
    bookindex = indexes[title]

    # get similar books from cosinesim matrix
    similarbooks = list(enumerate(cosinesim[bookindex]))

    # sort books by descending similarity
    similarbooks = sorted(similarbooks, key=lambda x: x[1], reverse=True)

    # get top 10 most similar books
    similarbooks = similarbooks[1:11]
    books = [b[0] for b in similarbooks]
    return df[['Title', 'Price', 'Genre']].iloc[books]

def budgetcheck(budget):
    '''This function compares the prices of the recommended similar books to the budget
        budget: string
        Returns
        recommendations: a list of recommended books within the given budget
    '''
    # get cosine similarity and indexes of list of books for recommendation in database  
    cosinesim, indexes = recommendationconfig(df)
    # use results to get top 10 most similar books
    result = getrecommendedbooks(mostpopularbk[0]['Title'], cosinesim, indexes)
    books = result.to_dict(orient = 'records')
    sum = 0
    # stores indexes books within recommended list that can be afforded
    affordableBooks = []
    # stores actual book records using indexes from affordableBooks
    recommendations = []

    # compare price of books to given budget
    for i in range(len(books)):
        if (sum + books[i]['Price']) < int(budget):
            affordableBooks.append(i)
            sum = sum + books[i]['Price']

    for i in affordableBooks:
        recommendations.append(books[i])

    return recommendations

def createGraphs():
    '''This function creates graphs showing  statistics that should help the librarian
        decided whether it is necessary to purchase new books or not.
        Returns
        fig: three subplots
    '''
    # get data for log count of book title and genre
    data = db.selectbookhistory()

    # get breakdown for most requested book in terms of Reservation, Loan & Returned
    # the idea here is help the librarian decide if it is necessary to purchase books similar to it
    data2 = db.selectmostrequestedbook()

    titles  = []
    genres = []
    counts = []
    status = []
    requests = []

    for i in range(len(data)):
        titles.append(data[i]['Title'])
        genres.append(data[i]['Genre'])
        counts.append(data[i]['COUNT(*)'])
    
    for i in range(len(data2)):
        status.append(data2[i]['Status'])
        requests.append(data2[i]['COUNT(*)'])

    plt.rcParams['font.size'] = '5'
    plt.xticks(rotation = 45)

    fig = plt.figure(figsize=(5,3), facecolor="#e4e4e4")
    ax1 = fig.add_subplot(2,3,1)
    ax2 = fig.add_subplot(2,3,2)
    ax3 = fig.add_subplot(2,3,3)
    bar_colors = ['purple', 'grey', 'purple', 'grey', 'purple']
    ax1.bar(x = titles, height = counts, color = bar_colors)
    ax2.bar(x =  genres, height = counts, color = bar_colors)
    ax3.bar(x = status, height= requests, color = bar_colors[:3])
    ax3.set_xticklabels(["Returned", "Loan", "Reserved"])
    ax1.set_title('Top 5 books')
    ax2.set_title('Top 5 genres')
    ax3.set_title('Most Requested Book Stats')
    ax1.tick_params(labelrotation=45)
    ax2.tick_params(labelrotation=45)
    ax3.tick_params(labelrotation=45)
    ax1.set_ylabel('Book Requests')

    return fig

def reset():
    '''This function resets the database'''
    result = db.reset()
    if result:
        status = "Reset successful"
    else:
        status = "Reset unsuccessful"
    return status

def main():
    ###### testing ######
    #budgetcheck() calls recommendationconfig() and getrecommendedbooks()
    budget = budgetcheck(200)
    print(budget)

if __name__ =='__main__':
    print(main())




import pandas as pd
import re
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
# to give each word a frequency then do the idf(inverse document frequency)
# a vector for each title and compare against all titles in the dataset (vectors)
from sklearn.metrics.pairwise import cosine_similarity
# compare similarities of entered title and titles in the dataset

moviesDF = pd.read_csv("movies.csv")
moviesDF

def cleanTitle(title):
    cleaned = re.sub("[^a-zA-Z0-9 ]", "", title)
    # cleaned = title.replace("(", "")
    # cleaned = cleaned.replace(")", "")
    return cleaned

# moviesDF.drop("clean_title", inplace=True, axis=1)
moviesDF["cleanTitle"] = moviesDF["title"].apply(cleanTitle)
moviesDF

vectorizer = TfidfVectorizer(ngram_range=(1,2))
# bigram, look for each two words together
tfidf = vectorizer.fit_transform(moviesDF["cleanTitle"])
# turn the set of titles into a matrix (sets ofnumbers)

def search(title):
    title = cleanTitle(title)
    queryVec = vectorizer.transform([title]) # turn the entered search title into set of numbers
    similarity = cosine_similarity(queryVec, tfidf).flatten() # compare query term to each of dataset titles and see the similarities
    # indices = np.argmax(similarity)
    # indices = np.argsort(similarity)[-5:][::-1]
    indices = np.argpartition(similarity, -5) [-5:]
    result = moviesDF.iloc[indices][::-1]
    return result # [['title','genres']]
# search("batman")

# pickle.dump(moviesDF.to_dict(),open('MoviesF.pkl','wb'))

ratingsDF = pd.read_csv("ratings.csv")
ratingsDF

def findRecommendations(movieID):
    similarUsers = ratingsDF[(ratingsDF["movieId"] == movieID) & (ratingsDF["rating"] >= 4)]["userId"].unique() # users who liked the same movie as us
    usersRecs = ratingsDF[(ratingsDF["userId"].isin(similarUsers)) & (ratingsDF["rating"] >=4)]["movieId"] # gets the movies liked by those users
    usersRecs = usersRecs.value_counts() / len(similarUsers)
    usersRecs = usersRecs[usersRecs> 0.10] # need movies that are recommended more than 10% from the users

    allUsers = ratingsDF[(ratingsDF["movieId"].isin(usersRecs.index)) & (ratingsDF["rating"] >= 4)] # all users who liked the movies the users who like our movie likes
    allUsersRecs = allUsers["movieId"].value_counts() / len(allUsers["userId"].unique())

    recsPerc = pd.concat([usersRecs, allUsersRecs], axis=1)
    recsPerc.columns = ["similar", "all"]

    recsPerc["score"] = recsPerc['similar'] / recsPerc['all']
    recsPerc = recsPerc.sort_values("score", ascending=False)

    mergedPercentages = recsPerc.head(20).merge(moviesDF, left_index=True, right_on="movieId") [["score", "title", "genres"]]
    return mergedPercentages



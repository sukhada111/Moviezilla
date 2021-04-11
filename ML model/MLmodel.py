import numpy as np
import pandas as pd
import ast
import pickle

movie=pd.read_csv('../Dataset/tmdb_5000_movies.csv')
credits=pd.read_csv('../Dataset/tmdb_5000_credits.csv')

#merging datasets
final=pd.merge(movie,credits,left_on='id',right_on='movie_id')[['id','original_title','genres','keywords','overview','cast','crew']]

final.dropna(subset=['overview'],inplace=True)


genres=[]
def convert(s):
    l1=[]
    for i in ast.literal_eval(s):
        l1.append(i['name'])
        if i['name'] not in genres:
            genres.append(i['name'])
    text=l1[:]
   
    l1=[]
    return text

final['genres']=final['genres'].apply(convert)
final['keywords']=final['keywords'].apply(convert)
final['overview']=final['overview'].apply(lambda x : x.split(' '))

def fetch_cast(text):
    L=[]
    counter=0
    for i in ast.literal_eval(text):
            if counter<3:
                L.append(i['name'])
            else:
                break
            counter+=1
    L1=L[:]
    L.clear()
    return L1

final['cast']=final['cast'].apply(fetch_cast)

def fetch_director(text):
    L=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            L.append(i['name'])
            break
    L1=L[:]
    L.clear()
    return L1

final['crew']=final['crew'].apply(fetch_director)

final['tags']=final['genres']+final['keywords']+final['overview']+final['cast']+final['crew']

def remove_space(L):
    L1=[]
    for i in L:
        L1.append(i.replace(' ',''))
    
    L2=L1[:] 
    L1.clear()
    return L2

final['tags']=final['tags'].apply(remove_space)

final['tags']=final['tags'].apply(lambda x:" ".join(x))

final['tags']=final['tags'].apply(lambda x:x.lower())

def convert(name):
    return name.lower()

final['lower_title']=final['original_title'].apply(convert)

from sklearn.feature_extraction.text import CountVectorizer

cv=CountVectorizer(stop_words='english',max_features=10000)



X = cv.fit_transform(final['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity

similarity_matrix = cosine_similarity(X)



mov=np.array(final['lower_title'])

def recommend(movie_name):
    recs=[]
    movie_name=movie_name.lower()
    if movie_name in mov:
        movie_index=final[final['lower_title']== movie_name].index[0]

        L=sorted(list(enumerate(similarity_matrix[movie_index])),reverse=True,key=lambda x:x[1])

        
        for i in L[1:6]:
            print(final.iloc[i[0]]['original_title'])
            recs.append(final.iloc[i[0]]['original_title'])
        return recs
    else:
        return recs

# pickle.dump(cv, open('cv.sav','wb'))
# pickle.dump(similarity_matrix, open('similarity_matrix.sav','wb'))
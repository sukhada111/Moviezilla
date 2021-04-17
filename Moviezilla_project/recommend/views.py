
from django.shortcuts import render,redirect,get_object_or_404

from register.models import Genre
from django.contrib.auth.decorators import login_required
import requests
from .forms import WishlistForm


import numpy as np
import pandas as pd
import ast
import pickle
import os

movie_loc=os.getcwd()
credits_loc=os.getcwd()
movie=pd.read_csv(movie_loc+'/recommend/static/recommend/movies.csv')
credits=pd.read_csv(credits_loc+'/recommend/static/recommend/credits.csv')

# movie=pd.read_csv('C:/Users/sukha/Documents/Moviezilla/Moviezilla_project/recommend/static/recommend/movies.csv')
# credits=pd.read_csv('C:/Users/sukha/Documents/Moviezilla/Moviezilla_project/recommend/static/recommend/credits.csv')
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

#case for actor name entered to get recommendations
def convert_cast(name):
    l1=[]
    for i in name:
        l1.append(i.lower())
    return l1

final['lower_cast']=final['cast'].apply(convert_cast)

#list of lists of cast for each movie
listt_cast=final['lower_cast'].tolist()


#loading the saved pickle Models
# cv=pickle.load(open('C:/Users/sukha/Documents/Moviezilla/Moviezilla_project/recommend/static/recommend/cv.sav','rb'))
# similarity_matrix=pickle.load(open('C:/Users/sukha/Documents/Moviezilla/Moviezilla_project/recommend/static/recommend/similarity_matrix.sav','rb'))

#function to find similar movies, cases: movie name is entered or actor name is entered by user
def recommend(movie_name):
    recs=[]
    flag=0
    movie_name=movie_name.lower()
    
    #checking if movie name is present
    if movie_name in mov:
        flag=1
        
        movie_index=final[final['lower_title']== movie_name].index[0]
        
    #case when actor name is entered
    else:
        actor_name=movie_name.lower()
        # checking if its present
        for i in range(len(listt_cast)):
            if actor_name in listt_cast[i]:
                
                flag=2
                
                title= final.iloc[i]['lower_title']
                break
        if flag==2:
            movie_index=final[final['lower_title']== title].index[0]
        
        
    if flag==1 or flag==2:
        
        #finding movies similar to given movie
        L=sorted(list(enumerate(similarity_matrix[movie_index])),reverse=True,key=lambda x:x[1])
        
        #recommending top 5 most similar movies
        for i in L[1:6]:
            print(final.iloc[i[0]]['original_title'])
            recs.append(final.iloc[i[0]]['original_title'])
        return recs
    
    #if movie/actor name not present in dataset
    else:
        return recs
        

# Create your views here.

@login_required
def dashb(request):
    if request.method=='GET':
         genres=get_object_or_404(Genre,user=request.user)
         return render(request,'recommend/dashboard.html',{'gen':genres})

    else:
        genres=get_object_or_404(Genre,user=request.user)

        mov_name=request.POST['movie']
        
        # getting recommendations from ML model by passing movie name
        movies=recommend(mov_name)
       
        if (len(movies))>0:
            
            # url = "https://api.themoviedb.org/3/movie/550?api_key=e1ce9e59e555f9ca9c979f9212093620"
           
           
            film_data=[]
            for film in movies:
                    #search query
                    url="https://api.themoviedb.org/3/search/movie?api_key=e1ce9e59e555f9ca9c979f9212093620&query={}"
                    #using film name to search for movie details
                    r = requests.get(url.format(film)).json()
                  
                    #fetching the movie id 
                    film_id=r['results'][0]['id']

                    url_det="https://api.themoviedb.org/3/movie/{}?api_key=e1ce9e59e555f9ca9c979f9212093620"
                    
                    #using movie id to fetch other details of that movie
                    r = requests.get(url_det.format(film_id)).json()
                    
                    film_recom = {
                        'title':r['original_title'] ,
                        'genre':r['genres'][0]['name'],
                        'overview':r['overview'],
                        'poster_path': r['poster_path'],
                        'tagline': r['tagline'],
                        'budget':r['budget'],
                        'revenue':r['revenue'],
                        'vote_average':r['vote_average'],
                        'vote_count':r['vote_count'],
                    }
                    film_data.append(film_recom)
            # print(film_data)

            return render(request,'recommend/dashboard.html',{'film_data': film_data,'gen':genres})
        else:
            return render(request,'recommend/dashboard.html',{'error': 'No movies found.','gen':genres})


@login_required
def wishlist(request):
        form=WishlistForm(request.POST)
        movie=form.save(commit=False)
        movie.user=request.user
        movie.save()
        return redirect('userprofile')
        
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404

from register.models import Genre
from recommend.models import Wishlist
from django.contrib.auth.decorators import login_required
import requests

@login_required
def userprofile(request):
    genres=get_object_or_404(Genre,user=request.user)
    movies=get_list_or_404(Wishlist,user=request.user)
    print(movies)
    movv=[]
    for i in range(len(movies)):
        movv.append(movies[i].movie_name)

    film_data=[]
    for film in movv:
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
    return render(request,'userprofile/profile.html',{'gen':genres,'film_data':film_data})

# Create your views here.

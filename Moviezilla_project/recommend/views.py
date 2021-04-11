
from django.shortcuts import render,redirect,get_object_or_404

from register.models import Genre
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.

@login_required
def dashb(request):
    genres=get_object_or_404(Genre,user=request.user)
    url = "https://api.themoviedb.org/3/movie/550?api_key=e1ce9e59e555f9ca9c979f9212093620"
    films =['Fight Club', 'Beauty and the Beast'] 

    film_data=[]
    for film in films:
            r = requests.get(url.format(film)).json()
            film_recom = {
                'title': film,
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
    print(film_data)

    return render(request,'recommend/dashboard.html',{'film_data': film_data,'gen':genres})

# def recommend(request):
   

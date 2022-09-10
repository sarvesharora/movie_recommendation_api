import pickle 
import pandas as pd
from flask import Flask,make_response

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommenda(movie_id):
    if(len(movies[movies["movie_id"] == movie_id]) == 0):
        return []
        
    movie_index = movies[movies["movie_id"] == movie_id].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:6]
    arr = []
    for i in movie_list:
        arr.append(str(movies.iloc[i[0]].movie_id))
    return arr

def recommend(movie):
    print(movies)
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:6]
    arr = []
    for i in movie_list:
        arr.append(movies.iloc[i[0]].title)
    return arr


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/movie/<moviename>")
def recommend_movies(moviename):
    arr = recommend(moviename)
    return make_response(
        arr,
        200,
    )


@app.route("/movieid/<int:movie_id>")
def recommend_movie_with_id(movie_id):
    return recommenda(movie_id)


if __name__ == '__main__':
   app.run()

import streamlit as st
import pickle as pkl
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Set page config with icon
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

TMDB_API_KEY=os.getenv('TMDB_API_KEY')

movies=pkl.load(open('movies_list.pkl','rb'))
similarity=pkl.load(open('similarity.pkl','rb'))
st.header('🎥 Movie Recommender System 🍿')
movies_list=movies['title'].values
movies_id=movies['id'].values

selected=st.selectbox("🎬 Select movie from dropdown",movies_list)
n_of_movies=st.slider("🍿 Number of movies to recommend",1,100,5)

def fetch_poster(movie_id):
    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path='https://image.tmdb.org/t/p/w500'+poster_path
    return full_path

def recommand(moveis:str,n_of_movies=6):
    index=movies[movies['title']==moveis].index[0]
    distance=sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    for i,j in distance[1:n_of_movies+1]:
        movies_id=movies['id'][i]
        title = movies['title'][i]
        poster = fetch_poster(movies_id)
        yield title, poster

if st.button("✨ Show Recommendations ✨"):
    st.subheader(f'🌟 Top {n_of_movies} Recommendations 🌟')
    
    cols = st.columns(min(5, n_of_movies))
    placeholder_containers = []
    
    for i in range(n_of_movies):
        col_idx = i % len(cols)
        with cols[col_idx]:
            placeholder_containers.append(st.empty())
    
    for idx, (title, poster) in enumerate(recommand(selected, n_of_movies)):
        col_idx = idx % len(cols)
        with placeholder_containers[idx]:
            st.text(title)
            st.image(poster)
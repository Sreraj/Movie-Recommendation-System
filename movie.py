import streamlit as st
import pickle as pkl
import requests
import os

# Load API key from environment variable
API_KEY = os.getenv('TMDB_API_KEY')

def fetch_poster(movie_id):
    """
    Fetches the movie poster URL using the TMDB API.
    """
    url ="https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')  # Get the poster path
        if poster_path:  # Check if poster_path is not None
            return 'https://image.tmdb.org/t/p/w185' + poster_path
        else:
            return "https://via.placeholder.com/185"  # Fallback placeholder
    else:
        return "https://via.placeholder.com/185"  # Default placeholder image

# Load the movie list and similarity matrix
movies = pkl.load(open('movies_list.pkl', 'rb'))
movies_list = movies['title']
similarity = pkl.load(open('similarity.pkl', 'rb'))

def recommend(movie_name):
    """
    Recommends similar movies based on the input movie name.
    """
    try:
        movie_index = movies[movies['title'] == movie_name].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_poster = []

        for i in movie_list:
            recommended_movies.append(movies.iloc[i[0]]['title'])
            poster = fetch_poster(movies.iloc[i[0]]['id'])
            recommended_movies_poster.append(poster)

        return recommended_movies, recommended_movies_poster
    except Exception as e:
        st.error(f"Error: {e}")
        return [], []

# Streamlit UI
st.title("Movie Recommendation System")

select_movie_name = st.selectbox("Which movie do you like most?", movies_list)

if st.button("Recommend"):
    names, posters = recommend(select_movie_name)
    cols = st.columns(5)  # Create 5 equal columns for the movie posters
    for name, poster, col in zip(names, posters, cols):
        with col:
            st.text(name)
            st.image(poster)


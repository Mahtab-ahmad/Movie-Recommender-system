
import streamlit as st
import requests

st.set_page_config(layout="wide")


movies = pickle.load(open('movies.pkl','rb'))  # importing movies
# similarity = pickle.load(open('similarity.pkl','rb'))
with gzip.open('similarity.pkl.gz','rb') as f:
    similarity = pickle.load(f)


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b37cd62f324bf8ae593e1c3693c2004d'.format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # fetching the index
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # to hold the index

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]]['movie_id']))
    return recommended_movies ,recommended_movies_poster


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values,
)


if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    # for i in names:
    #     st.write(i)

    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i % 5]:
            st.text(names[i])
            st.image(posters[i])  #caption=names[i]


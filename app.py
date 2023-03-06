import streamlit as st
import pickle
import time
import requests

movie_list = pickle.load(open('./model/movies_list.pkl', 'rb'))
movies_list = movie_list['title'].values

similar = pickle.load(open('./model/similar_movies.pkl', 'rb'))

movies_inf = pickle.load(open('./model/movies_data.pkl', 'rb'))


def fetch_posters(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        print("Poster path not found in API response.")
        return None


def fetch_recommended_movies(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similar[movie_index]
    new_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
    recommend_movies_titles = []
    recommend_movies_posters=[]
    for i in new_movies_list:
        movies_id = movie_list.iloc[i[0]].movie_id
        recommend_movies_titles.append(movie_list.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_posters(movies_id))
    return recommend_movies_titles, recommend_movies_posters




st.title("MOVIE Recommender")
selected_movie = st.selectbox('Select Any Movie', movies_list)

st.write('You selected:', selected_movie)
if st.button('Recommend Movies'):
    with st.spinner('Wait for it...'):
        time.sleep(2)
    recommended_movie_titles, recommended_movie_posters = fetch_recommended_movies(selected_movie)
    col =[0]*5
    col = st.columns(5)


    for i in range(5):
        with col[i]:
            st.image(recommended_movie_posters[i])
            st.text(recommended_movie_titles[i])
    st.success('Done!')



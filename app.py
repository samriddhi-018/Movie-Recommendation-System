import streamlit as st
import pickle
import pandas as pd
import requests
import openai
import os

# Use an environment variable instead
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=07092e0af5440ee6f504e651f4f0e537&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dic.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System and ChatGPT')

# Movie Recommender Section
selected_movie_name = st.selectbox(
    'Choose any movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

# ChatGPT Section
st.header('Ask ChatGPT about movie preferences:')
user_input = st.text_input('You:')

if st.button('Ask ChatGPT'):
    # Combine user input with a prompt for ChatGPT
    prompt = f"I like {selected_movie_name}. {user_input}"

    # Generate a response from ChatGPT
    chatgpt_response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )

    # Display the response
    st.text("ChatGPT: " + chatgpt_response['choices'][0]['text'])

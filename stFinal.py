import streamlit as st
import mrF

st.title("Movie Recommandation System")
title = st.text_input("Type your Favourite Movie Name")

if st.button("Recommend"):
    results = mrF.search(title.capitalize())
    movieID = results.iloc[0]['movieId']
    mP = mrF.findRecommendations(movieID)
    st.write(mP)



# To run, write in cmd -> streamlit run stFinal.py

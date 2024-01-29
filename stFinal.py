import streamlit as st
import mrF # the python file that has the functions 

def typingSuggestions(input_text):    
    if len(input_text) >= 3:
        suggestions = mrF.moviesDF['title'].values
        return [suggestion for suggestion in suggestions if input_text.lower() in suggestion.lower()]
    else:
        return []
st.title("Movie Recommandation System")
title = st.text_input("Type your Favourite Movie Name")
# title = st.selectbox("Select Movie Name", mrF.moviesDF['title'].values)

suggestions = typingSuggestions(title)

if suggestions:
    st.markdown("Typing Suggestions:")
    # st.markdown("* " + "\n* ".join(suggestions))
    # numRows = len(suggestions) // 2 + (len(suggestions) % 2 > 0)

    for i in range(5):
        columns = st.columns(2)
        stI = i * 2  # calculate the start index for each row
        endI = min((i + 1) * 2, len(suggestions))  # calculate the end index for each row

        for j in range(stI, endI):
            # columns[j % 2].write(suggestions[j])
            columns[j % 2].write("* " + suggestions[j])
            
if st.button("Recommend"):
    results = mrF.search(title.capitalize())
    movieID = results.iloc[0]['movieId']
    mP = mrF.findRecommendations(movieID)
    st.write(mP)



# To run, write in cmd -> streamlit run stFinal.py

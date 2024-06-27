import streamlit as st

st.title("About Fin")

st.write("### Financial literacy is one of the most important skills.")
st.write("### Fin's goal is to demystify your finances.")

st.write("This is a basic prototype to enable founders to have educated conversations with experts around the industry.")

example_questions = ["What are my total holdings?", 
                     "What are my total equity holdings in Robin Hood?", 
                     "How does my net worth compare to last year?", 
                     "Could you explain estimated taxes and include details relevant to my financial situation?"]

st.write("Example questions:")
for question in example_questions:
    st.write(f"- {question}")
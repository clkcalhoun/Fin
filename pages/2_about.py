import streamlit as st

st.title("About Fin")

st.write("### Everyone has questions about their money.")
st.write("### Fin is here to answer them.")

st.write("This is a basic prototype to enable the founders to have educated conversations with experts around the industry.")

example_questions = ["What are my total holdings?", 
                     "What are my total equity holdings in Robin Hood?", 
                     "How does my net worth compare to last year?", 
                     "Could you explain estimated taxes and include details relevant to my financial situation?"]

st.write("Example questions:")
for question in example_questions:
    st.write(f"- {question}")
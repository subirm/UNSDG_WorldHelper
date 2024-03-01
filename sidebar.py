"""
This Python code snippet is designed to work with Streamlit, a popular library for creating web applications with Python. 
It defines a function build_sidebar that creates a sidebar for a web application, which includes an image,
some styled text, a set of buttons for popular questions, and a button to clear the chat history
"""

# Define a function to build the sidebar of the web application
import streamlit as st
import random

# Define a function to build the sidebar of the web application
def build_sidebar():
    popular_questions = [
        "What is the UNSDG goal 1?",
        "What % of countries would have halved poverty by 2030?",
        "How is India tracking towards gender equality?",
        "From where does UNSDG source its data?",
        "What effect has covid-19 had on poverty?",
    ]
    
    # Define a function to insert a question as a user's prompt into the chat
    def insert_as_users_prompt(**kwargs):
        if prompt := kwargs.get("prompt"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
    # Define a function to clear the chat history
    def clear_chat_history():
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you today?"}
        ]

    # Display an image in the sidebar
    st.image("./assets/pippy.jpg", width=200)
    # Display styled text as a header in the sidebar
    st.write(
        "<h1>Hi, I'm <font color='#ffcdc2'>WorldHelper</font> - your personal UNSDG Helper</h1>",
        unsafe_allow_html=True,
    )
    
    # Display styled text as a subheader in the sidebar
    st.write(
        "<h2>Ask me anything</h2>",
        unsafe_allow_html=True,
    )

    # Pick any 4 questions randomly from popular_questions
    selected_questions = random.sample(popular_questions, 4)
    
    # For each selected question, create a button in the sidebar
    for question in selected_questions:
        st.sidebar.button(
            question,
            on_click=insert_as_users_prompt,
            kwargs={"prompt": question},
            use_container_width=True,
        )
    # Add a separator line in the sidebar
    st.sidebar.markdown("---")
    # Add a button to clear the chat history
    st.sidebar.button("Clear Chat History", on_click=clear_chat_history, type="primary")

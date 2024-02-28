import streamlit as st
import random


def build_sidebar():
    popular_questions = [
        "What is the UNSDG goal 1?",
        "What % of countries would have halved poverty by 2030?",
        "How is India tracking towards gender equality?",
        "From where does UNSDG source its data?",
        "What effect has covid-19 had on poverty?",
    ]

    def insert_as_users_prompt(**kwargs):
        if prompt := kwargs.get("prompt"):
            st.session_state.messages.append({"role": "user", "content": prompt})

    def clear_chat_history():
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you today?"}
        ]

    # App sidebar
    st.image("./assets/pippy.jpg", width=50)
    st.write(
        "<h1>Hi, I'm <font color='#ffcdc2'>WorldHelper</font> - your personal UNSDG Helper</h1>",
        unsafe_allow_html=True,
    )
    
    st.write(
        "<h2>Ask me anything</h2>",
        unsafe_allow_html=True,
    )

    # Pick any 4 questions randomly from popular_questions
    selected_questions = random.sample(popular_questions, 4)

    for question in selected_questions:
        st.sidebar.button(
            question,
            on_click=insert_as_users_prompt,
            kwargs={"prompt": question},
            use_container_width=True,
        )
    st.sidebar.markdown("---")
    st.sidebar.button("Clear Chat History", on_click=clear_chat_history, type="primary")

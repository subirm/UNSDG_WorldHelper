# First, we need to get our toolbox ready. This is like opening your art kit before you start painting.
import streamlit as st  # This is our toolbox for making websites.
import random  # This helps us pick random things, like drawing a random card from a deck.

# Now, we're going to set up our sidebar, which is like setting up your table with all your art supplies before you start a project.
def build_sidebar():
    # Here, we're making a list of questions, like writing down ideas on a piece of paper so we don't forget them.
    popular_questions = [
        "What is the UNSDG goal 1?",
        "What % of countries would have halved poverty by 2030?",
        "How is India tracking towards gender equality?",
        "From where does UNSDG source its data?",
        "What effect has covid-19 had on poverty?",
    ]
    
    # This is a special trick that lets us put one of the questions into our chat, like dropping a hint or suggestion into a conversation.
    def insert_as_users_prompt(**kwargs):
        if prompt := kwargs.get("prompt"):  # If we have a question to suggest,
            st.session_state.messages.append({"role": "user", "content": prompt})  # We add it to our chat like someone asked it.
            
    # This is a button that clears our chat, like shaking an etch-a-sketch to start over with a clean slate.
    def clear_chat_history():
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you today?"}  # We start fresh with a friendly greeting.
        ]

    # Now, we're going to decorate our sidebar with a picture, like putting a sticker on your notebook.
    st.image("./assets/pippy.jpg", width=200)  # This shows a picture in our sidebar.
    
    # We're also adding some fancy writing to our sidebar, like drawing a title on the cover of your project.
    st.write(
        "<h1>Hi, I'm <font color='#ffcdc2'>WorldHelper</font> - your personal UNSDG Helper</h1>",
        unsafe_allow_html=True,  # This lets us use special text styles.
    )
    
    # Here's another bit of fancy writing for our sidebar, like adding a subtitle under your project title.
    st.write(
        "<h2>Ask me anything</h2>",
        unsafe_allow_html=True,  # Again, this lets us make our text look special.
    )

    # We're going to pick 4 random questions from our list, like drawing ideas out of a hat to see what to work on next.
    selected_questions = random.sample(popular_questions, 4)
    
    # For each question we picked, we're making a button in the sidebar. 
    for question in selected_questions:
        st.sidebar.button(
            question,  # This is the text on the button, like labeling your tool with what it does.
            on_click=insert_as_users_prompt,  # This tells the button what to do when clicked: suggest the question in our chat.
            kwargs={"prompt": question},  # This tells the button which question to suggest.
            use_container_width=True,  # This makes sure the button fits nicely in our sidebar.
        )
        
    # We're adding a line to our sidebar, like drawing a line on your paper to separate different sections.
    st.sidebar.markdown("---")
    
    # Finally, we're adding a special button that clears our chat, like having an eraser to start your drawing over.
    st.sidebar.button("Clear Chat History", on_click=clear_chat_history, type="primary")
